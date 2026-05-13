"""
compute_coverage.py — 知识覆盖率计算（召回率）

输入: eval/gold/*.json (金标准) + kg_output/sciencedb_10_datasets_papers/*.json (提取结果)
输出: coverage per type + macro/micro average

匹配策略:
  1. 同类型
  2. evidence 关键词交集 >= 阈值
  3. 结构化字段相似度 (Jaccard for term names)
"""

import json
import re
from pathlib import Path
from collections import defaultdict
from typing import Optional


GOLD_DIR = Path(__file__).parent / "gold"
KG_DIR = Path(__file__).parent.parent / "kg_output" / "sciencedb_10_datasets_papers"

TYPE_ORDER = ["concept", "relation", "dataset", "method", "experiment",
              "quantitative_result", "performance_result", "data_specification",
              "claim", "conclusion", "limitation", "future_work"]

# 有结构化字段的类型及其匹配字段
TYPE_KEY_FIELDS = {
    "concept": ["term", "normalized"],
    "relation": ["head_term", "tail_term", "relation_type"],
    "dataset": ["name"],
    "method": ["name", "method_type"],
    "experiment": ["task"],
    "quantitative_result": ["quantity", "context"],
    "performance_result": ["metric"],
    "data_specification": ["spec_type"],
}


def tokenize(text: str) -> set[str]:
    """简单分词：英文单词 + 中文单字"""
    words = set(re.findall(r"[a-zA-Z]+", text.lower()))
    words.update(re.findall(r"[一-鿿]", text))
    return words


def keyword_similarity(a: str, b: str) -> float:
    """Jaccard similarity of tokenized texts."""
    ta, tb = tokenize(a), tokenize(b)
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


def field_similarity(entry: dict, gold_entry: dict, etype: str) -> float:
    """计算结构化字段的匹配度。"""
    fields = TYPE_KEY_FIELDS.get(etype, [])
    if not fields:
        return 1.0  # 无字段的类型（如 conclusion）视为匹配
    scores = []
    for f in fields:
        v1 = str(entry.get(f, "") or "").lower()
        v2 = str(gold_entry.get(f, "") or gold_entry.get("correct_fields", {}).get(f, "") or "").lower()
        if v1 and v2:
            scores.append(keyword_similarity(v1, v2))
    return sum(scores) / len(scores) if scores else 0.0


def match_entry(extracted: dict, gold_entry: dict) -> Optional[dict]:
    """
    判断 extracted entry 是否匹配 gold entry。
    返回匹配信息或 None。
    """
    etype = gold_entry["type"]
    if extracted.get("type") != etype:
        return None

    ev = extracted.get("evidence", {}).get("original_text", "")
    gold_kw = gold_entry.get("evidence_keywords", [])
    gold_text = gold_entry.get("evidence_text", "")

    # evidence 关键词匹配
    kw_hits = sum(1 for kw in gold_kw if kw.lower() in ev.lower())
    kw_score = kw_hits / len(gold_kw) if gold_kw else 0.5

    # evidence 文本相似度
    txt_sim = keyword_similarity(ev, gold_text) if gold_text else 0.5

    # 字段相似度
    field_sim = field_similarity(extracted, gold_entry, etype)

    # 综合分数
    score = 0.4 * kw_score + 0.3 * txt_sim + 0.3 * field_sim

    if score >= 0.3:  # 放宽阈值，人工标注后用更严格的
        return {"extracted_id": extracted.get(TYPE_ID_FIELDS.get(etype, ""), ""),
                "score": round(score, 3),
                "kw_hits": kw_hits,
                "txt_sim": round(txt_sim, 3),
                "field_sim": round(field_sim, 3)}
    return None


TYPE_ID_FIELDS = {
    "concept": "concept_id", "relation": "relation_id", "dataset": "dataset_id",
    "method": "method_id", "experiment": "experiment_id",
    "quantitative_result": "qr_id", "performance_result": "perf_id",
    "data_specification": "ds_id", "conclusion": "conclusion_id",
    "claim": "claim_id", "future_work": "future_work_id", "limitation": "limitation_id",
}


def load_extracted(stem: str) -> dict:
    path = KG_DIR / f"{stem}.json"
    if not path.exists():
        return {"entries": []}
    return json.loads(path.read_text(encoding="utf-8"))


def load_gold(stem: str) -> dict:
    path = GOLD_DIR / f"{stem}.json"
    if not path.exists():
        return {"entries_eval": []}
    return json.loads(path.read_text(encoding="utf-8"))


def compute_coverage(stem: str) -> dict:
    """计算单篇论文的知识覆盖率。"""
    extracted = load_extracted(stem)
    gold = load_gold(stem)

    gold_entries = gold.get("entries_eval", [])
    # 只计算 action 不是 "remove" 的 gold entries
    gold_valid = [g for g in gold_entries if g.get("action") != "remove"]

    extracted_entries = extracted.get("entries", [])

    type_recall = defaultdict(lambda: {"gold": 0, "matched": 0})
    matched_gold = 0
    total_matches = []

    for ge in gold_valid:
        etype = ge["type"]
        type_recall[etype]["gold"] += 1

        best = None
        best_score = 0
        for ee in extracted_entries:
            m = match_entry(ee, ge)
            if m and m["score"] > best_score:
                best = m
                best_score = m["score"]

        if best and best_score >= 0.4:
            type_recall[etype]["matched"] += 1
            matched_gold += 1
            total_matches.append({"gold": ge.get("entry_id", ""), "extracted": best["extracted_id"], "score": best_score})

    # recall per type
    recall_by_type = {}
    for t in TYPE_ORDER:
        g = type_recall[t]["gold"]
        m = type_recall[t]["matched"]
        recall_by_type[t] = {"gold": g, "matched": m, "recall": round(m / g, 3) if g > 0 else None}

    macro_recall = round(
        sum(v["recall"] for v in recall_by_type.values() if v["recall"] is not None) /
        max(1, sum(1 for v in recall_by_type.values() if v["recall"] is not None)), 3)

    micro_recall = round(matched_gold / len(gold_valid), 3) if gold_valid else 0

    # precision: LLM 抽了多少正确的
    gold_action_correct = [g for g in gold_entries if g.get("action") == "correct"]
    n_extracted = len(extracted_entries)
    # 用 gold 中 "correct" 条目数 / 总提取条目数作为 precision 近似
    # 更准确的需要对每个 extracted entry 做 evaluation
    precision_approx = round(len(gold_action_correct) / n_extracted, 3) if n_extracted else 0

    return {
        "stem": stem,
        "recall_by_type": recall_by_type,
        "macro_recall": macro_recall,
        "micro_recall": micro_recall,
        "precision_approx": precision_approx,
        "gold_total": len(gold_valid),
        "extracted_total": n_extracted,
        "matched_count": matched_gold,
        "matches": total_matches,
    }


def main():
    results = []
    for gf in sorted(GOLD_DIR.glob("*.json")):
        stem = gf.stem
        r = compute_coverage(stem)
        results.append(r)

    if not results:
        print("没有找到金标准文件。请先在 eval/gold/ 中放置标注好的 JSON。")
        return

    print(f"{'='*70}")
    print(f"知识覆盖率评估 ({len(results)} 篇论文)")
    print(f"{'='*70}")

    avg_macro = sum(r["macro_recall"] for r in results) / len(results)
    avg_micro = sum(r["micro_recall"] for r in results) / len(results)
    avg_precision = sum(r["precision_approx"] for r in results) / len(results)

    print(f"\n综合指标:")
    print(f"  Macro Recall:  {avg_macro:.1%}  (各类别召回率均值)")
    print(f"  Micro Recall:  {avg_micro:.1%}  (条目级召回率)")
    print(f"  Precision 近似: {avg_precision:.1%}  (gold中标注correct的条目/总提取条目)")

    print(f"\n各类型召回率:")
    print(f"  {'类型':<22} {'gold':>5} {'matched':>8} {'recall':>7}")
    print(f"  {'-'*42}")
    for t in TYPE_ORDER:
        total_g = sum(r["recall_by_type"][t]["gold"] for r in results)
        total_m = sum(r["recall_by_type"][t]["matched"] for r in results)
        rec = round(total_m / total_g, 3) if total_g > 0 else None
        rec_str = f"{rec:.1%}" if rec is not None else "N/A"
        print(f"  {t:<22} {total_g:>5} {total_m:>8} {rec_str:>7}")

    print()
    for r in results:
        print(f"  {r['stem'][:55]:<55} macro={r['macro_recall']:.1%} micro={r['micro_recall']:.1%} gold={r['gold_total']} ext={r['extracted_total']} matched={r['matched_count']}")


if __name__ == "__main__":
    main()
