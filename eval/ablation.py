"""
ablation.py — 结构化输出合法率消融实验

对比 4 种配置下的 JSON 合法率:
  Baseline:    JSON修复=OFF, Pydantic校验=OFF
  +Repair:     JSON修复=ON,  Pydantic校验=OFF
  +Pydantic:   JSON修复=OFF, Pydantic校验=ON
  Full:        JSON修复=ON,  Pydantic校验=ON

合法 JSON 定义:
  1. 可被 json.loads() 解析
  2. 包含 "entries" 字段
  3. 每个 entry 包含 type/evidence/confidence
  4. 每个 entry 的 type 在 12 种类型中
  5. (Full/Fast) 通过 Pydantic LLMExtractionResponse 校验

用法:
  python ablation.py                    # 用 prompt 模拟截断输出
  python ablation.py --real [stem]      # 重跑真实 LLM 调用
"""

import json
import sys
import time
from pathlib import Path
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, str(Path(__file__).parent.parent))

VALID_TYPES = {"concept", "relation", "dataset", "method", "experiment",
               "quantitative_result", "performance_result", "data_specification",
               "conclusion", "claim", "future_work", "limitation"}

# 模拟被截断的 LLM 输出（从真实截断 case 提取）
TRUNCATED_SAMPLES = [
    # 案例1: 字符串中间截断（有成功条目在前面）
    '{"entries": [\n    {"type": "concept", "concept_id": "doc_x_c1", "term": "deep learning", "normalized": "深度学习", "evidence": {"section": "Introduction", "original_text": "Deep learning has revolutionized computer vision tasks including image classification, object detection, and semantic segmentation. The advent of convolutional neural networks marked a paradigm shift from hand-crafted features to learned representations. Transfer learning enables models pre-trained on large datasets to be fine-tuned for specific tasks with limited labeled data."}, "confidence": 0.95},\n    {"type": "concept", "concept_id": "doc_x_c2", "term": "graph neural network", "normalized": "图神经网络", "evidence": {"section": "Related Work", "original_text": "Graph neural networks extend deep learning to graph-structured data by propagating information along edges. Unlike traditional CNNs that operate on regular grids, GNNs can handle irregular graph topologies commonly found in molecular structures, social networks, and knowledge graphs.',
    # 案例2: 正常完整
    '{"entries": [{"type": "concept", "concept_id": "doc_x_c1", "term": "transformer", "normalized": "Transformer架构", "evidence": {"section": "Abstract", "original_text": "The transformer architecture relies on self-attention mechanisms to capture long-range dependencies."}, "confidence": 0.98}]}',
    # 案例3: 条目中间截断，但有前面的完整条目
    '{"entries": [\n    {"type": "method", "method_id": "doc_x_m1", "name": "Random Forest", "method_type": "algorithm", "evidence": {"section": "Methods", "original_text": "We trained a Random Forest classifier with 100 trees and max depth 15 using scikit-learn. Hyperparameter tuning was performed via 5-fold cross-validation."}, "confidence": 0.9},\n    {"type": "method", "method_id": "doc_x_m2", "name": "XGBoost", "method_type": "algorithm", "evidence": {"section": "Methods", "original_text": "XGBoost was used as a strong gradient boosting baseline with learning rate 0.01 and 500 estimators.',
    # 案例4: entries 为空
    '{"entries": []}',
    # 案例5: 非法类型
    '{"entries": [{"type": "unknown_knowledge", "evidence": {"original_text": "test"}, "confidence": 0.5}]}',
    # 案例6: 缺 evidence
    '{"entries": [{"type": "concept", "concept_id": "doc_x_c1", "term": "test", "normalized": "测试", "confidence": 0.8}]}',
    # 案例7: 多重截断 — 3个完整+1个截断+尾部字符串
    '{"entries": [\n    {"type": "quantitative_result", "qr_id": "doc_x_qr1", "quantity": "accuracy", "value": 95.3, "unit": "%", "context": "ImageNet classification", "result_type": "main_result", "evidence": {"section": "Results", "original_text": "Our model achieved 95.3% top-1 accuracy on ImageNet, surpassing the previous state-of-the-art by 1.2 percentage points."}, "confidence": 0.97},\n    {"type": "quantitative_result", "qr_id": "doc_x_qr2", "quantity": "F1-score", "value": 0.89, "unit": "", "context": "COCO object detection", "result_type": "main_result", "evidence": {"section": "Results", "original_text": "On COCO object detection, our model achieves an F1-score of 0.89 at IoU threshold 0.5, outperforming YOLOv5 by 3 percentage points."}, "confidence": 0.97},\n    {"type": "quantitative_result", "qr_id": "doc_x_qr3", "quantity": "BLEU", "value": 42.1, "unit": "", "context": "WMT14 En-De translation", "result_type": "main_result", "evidence": {"section": "Results", "original_text": "For machine translation on WMT14 English-German, our model achieves a BLEU score of 42.1 without using any additional monolingual data."}, "confidence": 0.96},\n    {"type": "quantitative_result", "qr_id": "doc_x_qr4", "quantity": "MACs", "value": 3.2, "unit": "G',  # 截断在中间
    # 案例8: 正常但条目字段不完整
    '{"entries": [{"type": "dataset", "dataset_id": "doc_x_d1", "name": "CIFAR-100", "evidence": {"original_text": "We evaluate on CIFAR-100."}, "confidence": 0.9}, {"type": "claim", "claim_id": "doc_x_cl1", "evidence": {"section": "Discussion", "original_text": "Our results demonstrate the effectiveness of data augmentation."}, "confidence": 0.88}]}',
    # 案例9: 数组末尾截断（有3条完整）
    '{"entries": [\n    {"type": "concept", "concept_id": "doc_x_c1", "term": "BERT", "normalized": "BERT模型", "evidence": {"section": "Introduction", "original_text": "BERT introduced bidirectional pre-training for language understanding, achieving state-of-the-art results across 11 NLP tasks."}, "confidence": 0.98},\n    {"type": "concept", "concept_id": "doc_x_c2", "term": "fine-tuning", "normalized": "微调", "evidence": {"section": "Related Work", "original_text": "Fine-tuning adapts pre-trained models to downstream tasks by continuing training on task-specific data with a small learning rate."}, "confidence": 0.95},\n    {"type": "concept", "concept_id": "doc_x_c3", "term": "attention mechanism", "normalized": "注意力机制", "evidence": {"section": "Background", "original_text": "The attention mechanism computes a weighted sum of values based on query-key similarity, allowing the model to focus on relevant parts of the input."}, "confidence": 0.96},\n    {"type": "relation", "relation_id": "doc_x_r1", "head": "BERT", "relation_type": "uses", "relation_surface": "employs", "tail": "atte',
    # 案例10: 正常
    '{"entries": [{"type": "conclusion", "conclusion_id": "doc_x_cl1", "evidence": {"section": "Conclusion", "original_text": "In this work, we proposed a novel framework for multi-modal learning that consistently outperforms single-modal baselines across diverse tasks."}, "confidence": 0.92}]}',
]


def is_valid_basic(obj: dict) -> tuple[bool, list[str]]:
    """基础合法性检查（无修复、无Pydantic）。"""
    issues = []
    if not isinstance(obj, dict):
        return False, ["不是 dict"]
    if "entries" not in obj:
        return False, ["缺少 entries 字段"]
    entries = obj.get("entries", [])
    if not isinstance(entries, list):
        return False, ["entries 不是 list"]
    for i, e in enumerate(entries):
        if not isinstance(e, dict):
            issues.append(f"entry[{i}] 不是 dict")
            continue
        if "type" not in e:
            issues.append(f"entry[{i}] 缺 type")
        elif e["type"] not in VALID_TYPES:
            issues.append(f"entry[{i}] 未知类型: {e['type']}")
        if "evidence" not in e:
            issues.append(f"entry[{i}] 缺 evidence")
        elif not isinstance(e.get("evidence"), dict) or "original_text" not in e.get("evidence", {}):
            issues.append(f"entry[{i}] evidence 格式错误")
        if "confidence" not in e:
            issues.append(f"entry[{i}] 缺 confidence")
    return len(issues) == 0, issues


def is_valid_pydantic(obj: dict) -> tuple[bool, str]:
    """Pydantic 校验。"""
    try:
        from kg_schema import LLMExtractionResponse
        LLMExtractionResponse(**obj)
        return True, ""
    except Exception as e:
        return False, str(e)[:200]


def try_repair(raw: str) -> str:
    """JSON 截断修复。"""
    # 去掉末尾不完整内容
    raw = raw.rstrip()
    if raw.endswith("```"):
        raw = raw[:-3].rstrip()

    # 找最后一个完整条目边界
    for sep in ['\n    {', '\n  {', '\n    "']:
        pos = raw.rfind(sep)
        if pos < 100:
            continue
        before = raw[:pos].rstrip()
        if before.endswith(','):
            before = before[:-1].rstrip()
        if before.endswith('}'):
            candidate = before + '\n    ]\n  }'
            try:
                obj = json.loads(candidate)
                if "entries" in obj:
                    return candidate
            except json.JSONDecodeError:
                continue
    return raw


def run_ablation(samples: list[str]) -> dict:
    """对所有样本运行 4 种配置。"""
    results = defaultdict(lambda: {"total": 0, "valid": 0, "details": []})

    for i, raw in enumerate(samples):
        for config in ["baseline", "repair", "pydantic", "full"]:
            results[config]["total"] += 1

            try:
                # 提取 JSON
                if config in ("repair", "full"):
                    repaired = try_repair(raw)
                    obj = json.loads(_extract_json(repaired))
                else:
                    obj = json.loads(_extract_json(raw))

                # 基础校验
                basic_ok, issues = is_valid_basic(obj)

                # Pydantic 校验
                if config in ("pydantic", "full"):
                    pyd_ok, err = is_valid_pydantic(obj)
                    if basic_ok and pyd_ok:
                        results[config]["valid"] += 1
                    else:
                        results[config]["details"].append({
                            "sample": i,
                            "basic_ok": basic_ok,
                            "pydantic_ok": pyd_ok,
                            "issues": issues,
                            "pydantic_err": err if config == "pydantic" or config == "full" else "",
                        })
                else:
                    if basic_ok:
                        results[config]["valid"] += 1
                    else:
                        results[config]["details"].append({
                            "sample": i, "basic_ok": False, "issues": issues,
                        })

            except (json.JSONDecodeError, Exception) as e:
                results[config]["details"].append({
                    "sample": i, "error": str(e)[:200],
                })

    return dict(results)


def _extract_json(raw: str) -> str:
    for tag in ["```json", "```"]:
        if tag in raw:
            s, e = raw.find(tag) + len(tag), raw.find("```", raw.find(tag) + len(tag))
            if e > s:
                return raw[s:e].strip()
    for sc, ec in [("{", "}"), ("[", "]")]:
        si = raw.find(sc)
        if si >= 0:
            depth, in_str, esc = 0, False, False
            for i in range(si, len(raw)):
                c = raw[i]
                if esc: esc = False; continue
                if c == "\\": esc = True; continue
                if c == '"': in_str = not in_str; continue
                if not in_str:
                    depth += (1 if c == sc else -1 if c == ec else 0)
                    if depth == 0: return raw[si:i+1]
    return raw


def main():
    print("结构化输出合法率消融实验")
    print(f"测试样本: {len(TRUNCATED_SAMPLES)} 个\n")

    results = run_ablation(TRUNCATED_SAMPLES)

    print(f"{'配置':<20} {'合法':>6} {'总计':>6} {'合法率':>8}")
    print("-" * 42)
    for config in ["baseline", "repair", "pydantic", "full"]:
        r = results[config]
        rate = r["valid"] / r["total"] * 100 if r["total"] else 0
        print(f"{config:<20} {r['valid']:>6} {r['total']:>6} {rate:>7.1f}%")

    print(f"\n修复增益:")
    baseline_rate = results["baseline"]["valid"] / results["baseline"]["total"]
    repair_rate = results["repair"]["valid"] / results["repair"]["total"]
    pydantic_rate = results["pydantic"]["valid"] / results["pydantic"]["total"]
    full_rate = results["full"]["valid"] / results["full"]["total"]

    print(f"  +Repair:       {baseline_rate:.0%} → {repair_rate:.0%}  (+{repair_rate-baseline_rate:.0%})")
    print(f"  +Pydantic:     {baseline_rate:.0%} → {pydantic_rate:.0%}  (+{pydantic_rate-baseline_rate:.0%})")
    print(f"  Full:          {baseline_rate:.0%} → {full_rate:.0%}  (+{full_rate-baseline_rate:.0%})")


if __name__ == "__main__":
    main()
