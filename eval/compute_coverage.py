"""
compute_coverage.py — 知识覆盖率（召回率）

方法: 检索 + LLM 重排序
  1. 对每条金标准条目，从提取结果中筛选同 type
  2. 用字段关键词匹配打分，取 top-3 候选
  3. LLM 逐对判断: 是否表达同一知识点？
  4. 至少一个 Yes → 召回成功

输入: eval/gold/*.json + kg_output/sciencedb_10_datasets_papers/*.json
输出: 12 种类型的 recall + macro/micro average
"""

import json, sys, re
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

# 用于候选检索的字段
RETRIEVAL_FIELDS = {
    "concept":             ["term", "normalized", "std_label"],
    "relation":            ["head", "relation_type", "tail", "relation_surface"],
    "dataset":             ["name", "domain"],
    "method":              ["name"],
    "experiment":          ["task", "setup"],
    "quantitative_result": ["quantity", "context"],
    "performance_result":  ["metric", "compared_to"],
    "data_specification":  ["spec_type", "description"],
    "claim":               [],
    "conclusion":          [],
    "limitation":          [],
    "future_work":         [],
}

LLM_MATCH_PROMPT = """你是一位学术知识匹配专家。判断金标准条目和提取条目是否表达同一个知识点。

## 知识类型: {etype}"""

LLM_MATCH_USER = """## 金标准条目
字段: {gold_fields}
evidence: {gold_evidence}

## 提取条目
字段: {extracted_fields}
evidence: {extracted_evidence}

它们是否表达同一个知识点？只回答 yes 或 no。"""


def tokenize(text: str) -> set[str]:
    words = set(re.findall(r"[a-zA-Z0-9]+", str(text).lower()))
    words.update(re.findall(r"[一-鿿]", str(text)))
    return words


def retrieve_candidates(gold: dict, extracted_entries: list[dict]) -> list[dict]:
    """从提取结果中检索 top-3 候选。"""
    etype = gold["type"]
    ret_fields = RETRIEVAL_FIELDS.get(etype, [])

    # 构建 gold 的检索 token set
    gold_tokens = set()
    for f in ret_fields:
        gold_tokens.update(tokenize(str(gold.get(f, "") or gold.get("correct_fields", {}).get(f, ""))))

    scored = []
    for ee in extracted_entries:
        if ee.get("type") != etype:
            continue

        # 计算字段关键词重叠分
        ee_tokens = set()
        for f in ret_fields:
            ee_tokens.update(tokenize(str(ee.get(f, ""))))

        if not gold_tokens:
            # 无字段类型（claim等）：用 evidence 文本长度作为弱信号
            ev_len = len(ee.get("evidence", {}).get("original_text", ""))
            scored.append((ee, ev_len))
        else:
            overlap = len(gold_tokens & ee_tokens)
            scored.append((ee, overlap))

    # 按得分降序，取 top-3
    scored.sort(key=lambda x: -x[1])
    return [e for e, _ in scored[:3]]


def llm_match(client, model, gold: dict, candidate: dict) -> bool:
    """LLM 判断两条条目是否表达同一知识点。"""
    etype = gold["type"]
    ret_fields = RETRIEVAL_FIELDS.get(etype, [])

    gold_f = {f: gold.get(f, "") or gold.get("correct_fields", {}).get(f, "") for f in ret_fields}
    gold_ev = gold.get("evidence_text", gold.get("evidence", {}).get("original_text", ""))[:2000]

    cand_f = {f: candidate.get(f, "") for f in ret_fields}
    cand_ev = candidate.get("evidence", {}).get("original_text", "")[:2000]

    sys_p = LLM_MATCH_PROMPT.format(etype=etype)
    user_p = LLM_MATCH_USER.format(
        gold_fields=json.dumps(gold_f, ensure_ascii=False),
        gold_evidence=gold_ev,
        extracted_fields=json.dumps(cand_f, ensure_ascii=False),
        extracted_evidence=cand_ev,
    )

    try:
        resp = client.chat.completions.create(
            model=model, temperature=0.0, max_tokens=10,
            messages=[{"role": "system", "content": sys_p},
                      {"role": "user", "content": user_p}])
        return "yes" in (resp.choices[0].message.content or "").lower()
    except Exception:
        return False


def load_extracted(stem: str) -> dict:
    path = KG_DIR / f"{stem}.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {"entries": []}


def load_gold(stem: str) -> dict:
    path = GOLD_DIR / f"{stem}.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {"entries_eval": []}


def compute_coverage(stem: str, client, model) -> dict:
    extracted = load_extracted(stem)
    gold = load_gold(stem)

    gold_evals = gold.get("entries_eval", [])
    gold_valid = [g for g in gold_evals if g.get("action") != "remove"]
    extracted_entries = extracted.get("entries", [])

    type_recall = defaultdict(lambda: {"gold": 0, "matched": 0})
    used_candidates = set()  # 已匹配的 extracted entry 不再复用

    for gi, ge in enumerate(gold_valid):
        etype = ge["type"]
        type_recall[etype]["gold"] += 1

        candidates = [c for c in retrieve_candidates(ge, extracted_entries)
                      if id(c) not in used_candidates]

        matched = False
        for c in candidates:
            if llm_match(client, model, ge, c):
                matched = True
                used_candidates.add(id(c))
                break

        if matched:
            type_recall[etype]["matched"] += 1

    recall_by_type = {}
    for t in TYPE_ORDER:
        g = type_recall[t]["gold"]
        m = type_recall[t]["matched"]
        recall_by_type[t] = {"gold": g, "matched": m,
                             "recall": round(m / g, 3) if g > 0 else None}

    macro = round(sum(v["recall"] for v in recall_by_type.values() if v["recall"] is not None) /
                  max(1, sum(1 for v in recall_by_type.values() if v["recall"] is not None)), 3)
    micro = round(sum(v["matched"] for v in recall_by_type.values()) /
                  max(1, sum(v["gold"] for v in recall_by_type.values())), 3)

    return {
        "stem": stem,
        "recall_by_type": recall_by_type,
        "macro_recall": macro,
        "micro_recall": micro,
        "gold_total": sum(v["gold"] for v in recall_by_type.values()),
        "matched_total": sum(v["matched"] for v in recall_by_type.values()),
    }


def main():
    from kg_extract import load_config
    cfg = load_config()
    client = OpenAI(api_key=cfg["api_key"], base_url=cfg["base_url"] or None)
    model = cfg["model"]

    results = []
    for gf in sorted(GOLD_DIR.glob("*.json")):
        stem = gf.stem
        r = compute_coverage(stem, client, model)
        results.append(r)
        print(f"  {stem[:50]:<50} macro={r['macro_recall']:.1%} micro={r['micro_recall']:.1%} gold={r['gold_total']} matched={r['matched_total']}")

    if not results:
        print("没有找到金标准文件")
        return

    print(f"\n{'='*70}")
    print(f"  知识覆盖率（检索+LLM重排序）— {len(results)} 篇论文")
    print(f"{'='*70}")
    print(f"  {'类型':<22} {'金标准':>6} {'匹配':>6} {'召回率':>8}")
    print(f"  {'-'*42}")
    for t in TYPE_ORDER:
        tg = sum(r["recall_by_type"][t]["gold"] for r in results)
        tm = sum(r["recall_by_type"][t]["matched"] for r in results)
        rec = round(tm / tg, 3) if tg > 0 else None
        print(f"  {t:<22} {tg:>6} {tm:>6} {rec:>7.1%}" if rec is not None else f"  {t:<22} {tg:>6} {tm:>6} {'N/A':>7}")

    avg_macro = sum(r["macro_recall"] for r in results) / len(results)
    avg_micro = sum(r["micro_recall"] for r in results) / len(results)
    print(f"  {'-'*42}")
    print(f"  Macro Recall: {avg_macro:.1%}    Micro Recall: {avg_micro:.1%}")


if __name__ == "__main__":
    main()
