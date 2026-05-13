"""
compute_accuracy.py — Evidence 准确率评估 (LLM-as-Judge)

对已匹配的 (extracted_entry, gold_entry) 对，用 LLM 判断：
  1. evidence 原文是否真正支撑该知识声明？
  2. 字段值是否与 evidence 一致？
  3. evidence 是否足够详细 (>= 8 句)？

输出: 准确率 per type + 各类错误分布
"""

import json
import sys
import os
from pathlib import Path
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).parent.parent))
from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI

GOLD_DIR = Path(__file__).parent / "gold"
KG_DIR = Path(__file__).parent.parent / "kg_output" / "sciencedb_10_datasets_papers"

TYPE_ORDER = ["concept", "relation", "dataset", "method", "experiment",
              "quantitative_result", "performance_result", "data_specification",
              "claim", "conclusion", "limitation", "future_work"]

JUDGE_PROMPT = """你是一位学术论文知识抽取质量评估专家。判断一条知识条目的 evidence 是否准确。

## 评估维度
1. **evidence 匹配度** (1-5): evidence 原文是否真正支撑该知识声明？字段值是否与 evidence 一致？
2. **evidence 完整性** (1-5): 是否包含足够的背景、条件、对比信息（至少 5-7 句）？
3. **无幻觉** (是/否): evidence 内容是否全部来自原文（没有编造）？

## 输出格式
```json
{
  "evidence_match": 4,
  "completeness": 3,
  "no_hallucination": true,
  "issues": ["evidence 缺少对比基准的数值"],
  "brief": "一句话总结"
}
```"""


def load_extracted(stem: str) -> dict:
    path = KG_DIR / f"{stem}.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {"entries": []}


def load_gold(stem: str) -> dict:
    path = GOLD_DIR / f"{stem}.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def get_entry_by_id(entries: list, eid: str, id_field: str) -> dict | None:
    for e in entries:
        if e.get(id_field) == eid:
            return e
    return None


def judge_evidence(client, model, entry: dict) -> dict:
    """LLM 评估单条 evidence。"""
    etype = entry.get("type", "")
    ev = entry.get("evidence", {}).get("original_text", "")
    fields = {k: v for k, v in entry.items() if k not in ("type", "evidence", "confidence",
              "concept_id", "relation_id", "dataset_id", "method_id", "experiment_id",
              "perf_id", "qr_id", "ds_id", "conclusion_id", "claim_id", "future_work_id",
              "limitation_id")}

    user_prompt = f"""## 知识类型: {etype}
## 字段值: {json.dumps(fields, ensure_ascii=False)}
## evidence 原文:
{ev[:3000]}

请评估。"""

    try:
        resp = client.chat.completions.create(
            model=model, temperature=0.0, max_tokens=500,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": JUDGE_PROMPT},
                {"role": "user", "content": user_prompt},
            ])
        raw = resp.choices[0].message.content or ""
        return json.loads(raw)
    except Exception as e:
        return {"error": str(e), "evidence_match": 0, "completeness": 0, "no_hallucination": False}


def compute_accuracy(stem: str, client, model, limit: int = 20) -> dict:
    """评估单篇论文的 evidence 准确率。"""
    gold = load_gold(stem)
    extracted = load_extracted(stem)

    gold_evals = gold.get("entries_eval", [])
    extracted_entries = extracted.get("entries", [])

    # 采样：优先取 gold 中标注为 "correct" 的
    correct_evals = [g for g in gold_evals if g.get("action") == "correct"]
    sample = correct_evals[:limit]

    results = []
    type_scores = defaultdict(lambda: {"match": [], "completeness": [], "hallucination": []})

    for ge in sample:
        etype = ge["type"]
        entry_id = ge.get("entry_id", "")
        if not entry_id:
            continue

        id_field = next((v for k, v in {
            "concept": "concept_id", "relation": "relation_id", "dataset": "dataset_id",
            "method": "method_id", "experiment": "experiment_id",
            "quantitative_result": "qr_id", "performance_result": "perf_id",
            "data_specification": "ds_id", "conclusion": "conclusion_id",
            "claim": "claim_id", "future_work": "future_work_id", "limitation": "limitation_id",
        }.items() if k == etype), "")

        entry = get_entry_by_id(extracted_entries, entry_id, id_field)
        if not entry:
            continue

        judgment = judge_evidence(client, model, entry)
        judgment["entry_id"] = entry_id
        judgment["type"] = etype
        results.append(judgment)

        if "error" not in judgment:
            type_scores[etype]["match"].append(judgment["evidence_match"])
            type_scores[etype]["completeness"].append(judgment["completeness"])
            type_scores[etype]["hallucination"].append(1 if judgment.get("no_hallucination") else 0)

    # 汇总
    type_acc = {}
    for t in TYPE_ORDER:
        scores = type_scores[t]
        if scores["match"]:
            type_acc[t] = {
                "n": len(scores["match"]),
                "avg_match": round(sum(scores["match"]) / len(scores["match"]), 2),
                "avg_completeness": round(sum(scores["completeness"]) / len(scores["completeness"]), 2),
                "hallucination_rate": round(1 - sum(scores["hallucination"]) / len(scores["hallucination"]), 3),
            }

    all_match = [s for v in type_scores.values() for s in v["match"]]
    all_comp = [s for v in type_scores.values() for s in v["completeness"]]
    all_hall = [s for v in type_scores.values() for s in v["hallucination"]]

    return {
        "stem": stem,
        "evaluated": len(results),
        "type_accuracy": type_acc,
        "overall_avg_match": round(sum(all_match) / len(all_match), 2) if all_match else 0,
        "overall_avg_completeness": round(sum(all_comp) / len(all_comp), 2) if all_comp else 0,
        "overall_hallucination_rate": round(1 - sum(all_hall) / len(all_hall), 3) if all_hall else 0,
        "details": results,
    }


def main():
    from kg_extract import load_config
    cfg = load_config()
    if not cfg["api_key"]:
        print("错误: 未设置 OPENAI_API_KEY")
        return

    client = OpenAI(api_key=cfg["api_key"], base_url=cfg["base_url"] or None)
    model = cfg["model"]
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 20

    results = []
    for gf in sorted(GOLD_DIR.glob("*.json")):
        stem = gf.stem
        r = compute_accuracy(stem, client, model, limit=limit)
        results.append(r)
        print(f"  {stem[:50]:<50} eval={r['evaluated']}条 match={r['overall_avg_match']:.1f}/5 comp={r['overall_avg_completeness']:.1f}/5 hall={r['overall_hallucination_rate']:.1%}")

    if not results:
        print("没有找到金标准文件")
        return

    print(f"\n{'='*70}")
    print(f"Evidence 准确率综合评估")
    print(f"{'='*70}")

    avg_match = sum(r["overall_avg_match"] for r in results) / len(results)
    avg_comp = sum(r["overall_avg_completeness"] for r in results) / len(results)
    avg_hall = sum(r["overall_hallucination_rate"] for r in results) / len(results)

    print(f"\n  evidence 匹配度:    {avg_match:.1f}/5")
    print(f"  evidence 完整性:    {avg_comp:.1f}/5")
    print(f"  幻觉率:             {avg_hall:.1%}")

    # 按类型
    print(f"\n  各类型 accuracy:")
    type_aggr = defaultdict(lambda: {"match": [], "comp": [], "hall": []})
    for r in results:
        for t, v in r["type_accuracy"].items():
            type_aggr[t]["match"].append(v["avg_match"])
            type_aggr[t]["comp"].append(v["avg_completeness"])
            type_aggr[t]["hall"].append(v["hallucination_rate"])

    for t in TYPE_ORDER:
        ag = type_aggr[t]
        if ag["match"]:
            print(f"    {t:<22} match={sum(ag['match'])/len(ag['match']):.1f}/5  comp={sum(ag['comp'])/len(ag['comp']):.1f}/5  hall={sum(ag['hall'])/len(ag['hall']):.1%}  (n={len(ag['match'])}篇)")


if __name__ == "__main__":
    main()
