"""
compute_accuracy.py — Evidence 精确率评估

两步:
  1. Fidelity: evidence 原文能否在论文 MD 中找到（子串模糊匹配）？
  2. LLM-as-Judge: 该 evidence 是否真正支撑该知识声明？

输入: eval/gold/*.json + kg_output/sciencedb_10_datasets_papers/*.json + markdown/*.md
输出: per-type fidelity rate + LLM judge scores (match/completeness/hallucination)
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
MD_DIR = Path(__file__).parent.parent / "markdown" / "sciencedb_10_datasets_papers"

TYPE_ORDER = ["concept", "relation", "dataset", "method", "experiment",
              "quantitative_result", "performance_result", "data_specification",
              "claim", "conclusion", "limitation", "future_work"]

JUDGE_PROMPT = """你是一位学术论文知识抽取质量评估专家。判断一条知识条目的 evidence 是否准确。

## 评估
1. **evidence 支撑度 (1-5)**: evidence 原文是否真正支撑该知识声明？
   - 5: evidence 完整包含该知识的所有信息
   - 3: evidence 部分相关，但缺乏关键细节
   - 1: evidence 与该知识无关
2. **evidence 完整性 (1-5)**: evidence 是否包含足够的实验条件、数值、对比基准？
   - 5: 8+ 句完整段落
   - 3: 3-5 句，缺少部分上下文
   - 1: 1-2 句，过于简略
3. **无幻觉 (是/否)**: evidence 内容是否全部来自论文原文？

```json
{"evidence_match": 4, "completeness": 3, "no_hallucination": true, "brief": "一句话"}
```"""


def load_paper_md(stem: str) -> str:
    path = MD_DIR / f"{stem}.md"
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def check_fidelity(evidence: str, md_text: str) -> tuple[bool, float]:
    """检查 evidence 是否能在原文中找到。"""
    if not evidence or not md_text:
        return False, 0.0

    # 精确子串匹配
    if evidence[:100] in md_text:
        return True, 1.0

    # 分成 30-char chunks，统计命中率
    chunks = [evidence[i:i+50] for i in range(0, len(evidence), 25)]
    hits = sum(1 for c in chunks if len(c) > 20 and c in md_text)
    rate = hits / len(chunks) if chunks else 0
    return rate > 0.5, round(rate, 2)


def judge_evidence(client, model, entry: dict) -> dict:
    """LLM 评判 evidence 是否支撑该知识。"""
    etype = entry.get("type", "")
    ev = entry.get("evidence", {}).get("original_text", "")
    fields = {k: v for k, v in entry.items()
              if k not in ("type", "evidence", "confidence",
                           "concept_id", "relation_id", "dataset_id", "method_id",
                           "experiment_id", "perf_id", "qr_id", "ds_id",
                           "conclusion_id", "claim_id", "future_work_id", "limitation_id")}

    user_prompt = f"知识类型: {etype}\n字段值: {json.dumps(fields, ensure_ascii=False)}\n\nevidence:\n{ev[:3000]}"

    try:
        resp = client.chat.completions.create(
            model=model, temperature=0.0, max_tokens=500,
            response_format={"type": "json_object"},
            messages=[{"role": "system", "content": JUDGE_PROMPT},
                      {"role": "user", "content": user_prompt}])
        return json.loads(resp.choices[0].message.content or "{}")
    except Exception as e:
        return {"error": str(e), "evidence_match": 0, "completeness": 0, "no_hallucination": False}


def compute_accuracy(stem: str, client, model, limit: int = 20) -> dict:
    gold = json.loads((GOLD_DIR / f"{stem}.json").read_text(encoding="utf-8"))
    extracted = json.loads((KG_DIR / f"{stem}.json").read_text(encoding="utf-8"))
    md_text = load_paper_md(stem)

    # 取 gold 中标注为 correct 的条目
    correct_ids = {g["entry_id"] for g in gold.get("entries_eval", [])
                   if g.get("action") == "correct" and g.get("entry_id")}

    id_field_map = {
        "concept": "concept_id", "relation": "relation_id", "dataset": "dataset_id",
        "method": "method_id", "experiment": "experiment_id",
        "quantitative_result": "qr_id", "performance_result": "perf_id",
        "data_specification": "ds_id",
        "conclusion": "conclusion_id", "claim": "claim_id",
        "future_work": "future_work_id", "limitation": "limitation_id",
    }

    entries_to_eval = []
    for e in extracted.get("entries", []):
        eid = e.get(id_field_map.get(e.get("type", ""), ""), "")
        if eid in correct_ids:
            entries_to_eval.append(e)

    # 抽样
    if len(entries_to_eval) > limit:
        import random
        random.seed(42)
        entries_to_eval = random.sample(entries_to_eval, limit)

    results = []
    type_scores = defaultdict(lambda: {"fidelity": [], "match": [], "comp": [], "hall": []})

    for e in entries_to_eval:
        etype = e["type"]
        ev = e.get("evidence", {}).get("original_text", "")

        # Step 1: Fidelity
        fid_ok, fid_rate = check_fidelity(ev, md_text)

        # Step 2: LLM judge
        judgment = judge_evidence(client, model, e)
        eid = e.get(id_field_map.get(etype, ""), "")
        judgment["entry_id"] = eid
        judgment["fidelity"] = fid_ok
        judgment["fidelity_rate"] = fid_rate
        results.append(judgment)

        if "error" not in judgment:
            type_scores[etype]["fidelity"].append(1 if fid_ok else 0)
            type_scores[etype]["match"].append(judgment["evidence_match"])
            type_scores[etype]["comp"].append(judgment["completeness"])
            type_scores[etype]["hall"].append(1 if judgment.get("no_hallucination") else 0)

    type_acc = {}
    for t in TYPE_ORDER:
        s = type_scores[t]
        if s["match"]:
            type_acc[t] = {
                "n": len(s["match"]),
                "fidelity": round(sum(s["fidelity"]) / len(s["fidelity"]), 3),
                "avg_match": round(sum(s["match"]) / len(s["match"]), 2),
                "avg_comp": round(sum(s["comp"]) / len(s["comp"]), 2),
                "hall_rate": round(1 - sum(s["hall"]) / len(s["hall"]), 3),
            }

    all_m = [s for v in type_scores.values() for s in v["match"]]
    all_c = [s for v in type_scores.values() for s in v["comp"]]
    all_f = [s for v in type_scores.values() for s in v["fidelity"]]
    all_h = [s for v in type_scores.values() for s in v["hall"]]

    return {
        "stem": stem, "evaluated": len(results),
        "type_accuracy": type_acc,
        "avg_fidelity": round(sum(all_f) / len(all_f), 3) if all_f else 0,
        "avg_match": round(sum(all_m) / len(all_m), 2) if all_m else 0,
        "avg_comp": round(sum(all_c) / len(all_c), 2) if all_c else 0,
        "hall_rate": round(1 - sum(all_h) / len(all_h), 3) if all_h else 0,
    }


def main():
    from kg_extract import load_config
    cfg = load_config()
    client = OpenAI(api_key=cfg["api_key"], base_url=cfg["base_url"] or None)
    model = cfg["model"]

    results = []
    for gf in sorted(GOLD_DIR.glob("*.json")):
        r = compute_accuracy(gf.stem, client, model)
        results.append(r)
        print(f"  {gf.stem[:50]:<50} eval={r['evaluated']}条 fid={r['avg_fidelity']:.0%} match={r['avg_match']:.1f}/5 comp={r['avg_comp']:.1f}/5 hall={r['hall_rate']:.1%}")

    if not results:
        print("没有找到金标准文件")
        return

    print(f"\n{'='*65}")
    print(f"  Evidence 精确率综合评估 ({len(results)} 篇)")
    print(f"{'='*65}")
    avg_fid = sum(r["avg_fidelity"] for r in results) / len(results)
    avg_match = sum(r["avg_match"] for r in results) / len(results)
    avg_comp = sum(r["avg_comp"] for r in results) / len(results)
    avg_hall = sum(r["hall_rate"] for r in results) / len(results)
    print(f"  evidence 原文命中率 (fidelity): {avg_fid:.1%}")
    print(f"  evidence 支撑度 (LLM judge):    {avg_match:.1f}/5")
    print(f"  evidence 完整性 (LLM judge):    {avg_comp:.1f}/5")
    print(f"  幻觉率:                          {avg_hall:.1%}")


if __name__ == "__main__":
    main()
