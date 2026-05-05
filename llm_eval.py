"""
llm_eval.py — LLM 知识抽取模型评估：Precision/Recall/F1/类型覆盖/成本估算

用法:
    python llm_eval.py                           # 评估所有有输出的模型
    python llm_eval.py --gold gold_xxx.json      # 指定 gold standard 文件
    python llm_eval.py --paper stem              # 指定论文（不含 .md）
"""

import json
import re
import sys
from pathlib import Path
from datetime import datetime, timezone

BASE_DIR = Path(__file__).parent
TEST_DIR = BASE_DIR / "llm_test"
GOLD_DIR = BASE_DIR / "gold_standard"
MARKDOWN_DIR = BASE_DIR / "markdown"

# ── 评分权重 ──
WEIGHTS = {
    "concept_f1": 0.35,
    "method_f1": 0.25,
    "type_coverage": 0.15,
    "discipline": 0.05,
    "token_efficiency": 0.10,
    "evidence_brevity": 0.10,
}
# Note: relation_f1 removed — no model currently extracts relations

ALL_TYPES = [
    "concept", "relation", "dataset", "method", "experiment",
    "performance_result", "conclusion", "claim", "future_work", "limitation"
]


def normalize_term(term: str) -> str:
    """标准化术语：小写 + 去标点 + 去多余空格"""
    term = term.lower().strip()
    term = re.sub(r'[\u2010-\u2015\-\u2018-\u201f\u2022\u2023\u2043\u2050\u2051\u2052\u2212]', ' ', term)
    term = re.sub(r'[^a-z0-9\s]', '', term)
    term = re.sub(r'\s+', ' ', term).strip()
    return term


def compute_f1(gold_set: set, pred_set: set) -> tuple[float, float, float]:
    tp = len(gold_set & pred_set)
    fp = len(pred_set - gold_set)
    fn = len(gold_set - pred_set)
    p = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    r = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * p * r / (p + r) if (p + r) > 0 else 0.0
    return p, r, f1


def load_gold(paper_stem: str) -> dict:
    """加载 gold standard 标注"""
    candidates = sorted(GOLD_DIR.glob(f"*{paper_stem}*"))
    if not candidates:
        # Try partial match (e.g., paper_stem has -main but gold file doesn't)
        core = paper_stem.rsplit("-", 1)[0] if "-" in paper_stem else paper_stem
        candidates = sorted(GOLD_DIR.glob(f"*{core}*"))
    if not candidates:
        candidates = sorted(GOLD_DIR.glob("gold_*.json"))
    if not candidates:
        print("错误: 未找到 gold standard 文件"); sys.exit(1)
    gold = json.loads(candidates[0].read_text(encoding="utf-8"))
    print(f"Gold standard: {candidates[0].name}")
    return gold


def extract_model_outputs(test_dir: Path, paper_stem: str) -> dict:
    """收集所有模型的抽取结果"""
    results = {}
    for model_dir in sorted(test_dir.iterdir()):
        if not model_dir.is_dir():
            continue
        out_file = model_dir / f"{paper_stem}.json"
        if not out_file.exists():
            continue
        data = json.loads(out_file.read_text(encoding="utf-8"))
        entries = data.get("entries", [])
        timing = {}
        test_info = data.get("test_info", {})
        results[model_dir.name] = {"entries": entries, "test_info": test_info}
    return results


def eval_one_model(entries: list, gold: dict, timing: dict = None) -> dict:
    """评估单个模型的抽取质量"""
    metrics = {}

    # ── Concept F1 ──
    gold_concepts = {normalize_term(c["term"]) for c in gold.get("concepts", [])}
    pred_concepts = {normalize_term(e["term"]) for e in entries if e["type"] == "concept"}
    cp, cr, cf1 = compute_f1(gold_concepts, pred_concepts)
    metrics["concept_precision"] = round(cp, 3)
    metrics["concept_recall"] = round(cr, 3)
    metrics["concept_f1"] = round(cf1, 3)
    metrics["concept_tp"] = len(gold_concepts & pred_concepts)
    metrics["concept_fp"] = len(pred_concepts - gold_concepts)
    metrics["concept_fn"] = len(gold_concepts - pred_concepts)
    metrics["concept_count"] = len(pred_concepts)

    # ── Method F1 ──
    gold_methods = {normalize_term(m["name"]) for m in gold.get("methods", [])}
    pred_methods = {normalize_term(e.get("name", "")) for e in entries if e["type"] == "method" and e.get("name")}
    mp, mr, mf1 = compute_f1(gold_methods, pred_methods)
    metrics["method_precision"] = round(mp, 3)
    metrics["method_recall"] = round(mr, 3)
    metrics["method_f1"] = round(mf1, 3)
    metrics["method_tp"] = len(gold_methods & pred_methods)
    metrics["method_fp"] = len(pred_methods - gold_methods)
    metrics["method_fn"] = len(gold_methods - pred_methods)

    # ── Relation F1 ──
    # Models output head/tail as concept_term names (from head_term/tail_term fields)
    gold_rels = {(normalize_term(r["head"]), normalize_term(r["tail"])) for r in gold.get("relations", [])}
    pred_rels = set()
    for e in entries:
        if e["type"] == "relation":
            h = normalize_term(e.get("head_term", ""))
            t = normalize_term(e.get("tail_term", ""))
            # Also try from head/tail if they're direct term references (not IDs)
            if not h:
                h = normalize_term(e.get("head", ""))
            if not t:
                t = normalize_term(e.get("tail", ""))
            if h and t:
                pred_rels.add((h, t))
    rp, rr, rf1 = compute_f1(gold_rels, pred_rels)
    metrics["relation_precision"] = round(rp, 3)
    metrics["relation_recall"] = round(rr, 3)
    metrics["relation_f1"] = round(rf1, 3)

    # ── Type Coverage ──
    present_types = {e["type"] for e in entries if e["type"] in ALL_TYPES}
    metrics["type_coverage"] = len(present_types)
    metrics["type_coverage_pct"] = round(len(present_types) / len(ALL_TYPES) * 100, 1)
    metrics["present_types"] = sorted(present_types)
    metrics["missing_types"] = sorted(set(ALL_TYPES) - present_types)

    # ── Per-type counts ──
    type_counts = {}
    for t in ALL_TYPES:
        type_counts[t] = sum(1 for e in entries if e["type"] == t)
    metrics["type_counts"] = type_counts
    metrics["total_entries"] = len(entries)

    # ── Discipline Accuracy ──
    metrics["discipline_match"] = 0

    # ── Token Efficiency ──
    comp_tokens = timing.get("completion_tokens", 0) if timing else 0
    prompt_tokens = timing.get("prompt_tokens", 0) if timing else 0
    metrics["prompt_tokens"] = prompt_tokens
    metrics["completion_tokens"] = comp_tokens
    if comp_tokens > 0 and len(entries) > 0:
        metrics["tokens_per_entry"] = round(comp_tokens / len(entries), 1)
    else:
        metrics["tokens_per_entry"] = 0

    # ── Evidence Brevity ──
    evidence_lengths = []
    for e in entries:
        ev = e.get("evidence", {})
        if ev:
            txt = ev.get("original_text", "")
            if txt:
                evidence_lengths.append(len(txt))
    if evidence_lengths:
        metrics["avg_evidence_len"] = round(sum(evidence_lengths) / len(evidence_lengths), 0)
    else:
        metrics["avg_evidence_len"] = 0

    return metrics


def compute_composite_score(metrics: dict, gold: dict) -> float:
    """计算综合评分 (0-100)"""
    # Concept F1 (0-100)
    concept_score = metrics["concept_f1"] * 100

    # Method F1 (0-100)
    method_score = metrics["method_f1"] * 100

    # Relation F1 (0-100)
    relation_score = metrics["relation_f1"] * 100

    # Type Coverage (0-100)
    coverage_score = metrics["type_coverage_pct"]

    # Discipline (0-100)
    discipline_score = metrics.get("discipline_match", 0) * 100

    # Token Efficiency (0-100): lower tokens/entry = higher score
    # Normalize: assume 50 tokens/entry is ideal, 500+ is bad
    tpe = metrics.get("tokens_per_entry", 0)
    if tpe > 0:
        token_score = max(0, 100 - (tpe - 50) / 4.5)
    else:
        token_score = 0

    # Evidence Brevity (0-100): shorter evidence = more concise
    # Ideal: 100-300 chars, too long = verbose
    ael = metrics.get("avg_evidence_len", 0)
    if ael > 0:
        evidence_score = max(0, 100 - abs(ael - 200) / 3)
    else:
        evidence_score = 0

    score = (
        WEIGHTS["concept_f1"] * concept_score +
        WEIGHTS["method_f1"] * method_score +
        WEIGHTS["type_coverage"] * coverage_score +
        WEIGHTS["discipline"] * discipline_score +
        WEIGHTS["token_efficiency"] * token_score +
        WEIGHTS["evidence_brevity"] * evidence_score
    )
    return round(score, 1)


def get_tokens_from_results_json(paper_stem: str) -> dict:
    """从 results.json 获取每个模型的 token 统计"""
    results_path = TEST_DIR / "results.json"
    if not results_path.exists():
        return {}
    data = json.loads(results_path.read_text())
    tokens = {}
    for pt in data.get("papers_tested", []):
        papers = pt.get("paper", [])
        if any(paper_stem in p for p in papers):
            tokens[pt["model"]] = {
                "prompt_tokens": pt.get("prompt_tokens", 0),
                "completion_tokens": pt.get("completion_tokens", 0),
                "total_time": pt.get("total_time", 0),
                "total_entries": pt.get("total_entries", 0),
            }
    return tokens


def print_ranking_table(all_results: list, gold: dict):
    """打印排名表"""
    header = (
        f"{'排名':>3} | {'模型':<25} | {'综合分':>5} | "
        f"Concept F1 | Method F1 | 类型覆盖 | Entries | Tokens/条 | 耗时"
    )
    sep = "-" * len(header)
    print(f"\n{'='*len(header)}")
    print("模型评估排名（按综合得分）")
    print(f"{'='*len(header)}")
    print(header)
    print(sep)
    for i, r in enumerate(all_results, 1):
        tpe = r["metrics"].get("tokens_per_entry", 0)
        time_val = r.get("time", 0)
        time_str = f"{time_val:.1f}s" if time_val > 0 else "-"
        print(
            f"{i:>3} | {r['model']:<25} | {r['score']:>5.1f} | "
            f"   {r['metrics']['concept_f1']:.3f}   | "
            f"  {r['metrics']['method_f1']:.3f}   | "
            f"  {r['metrics']['type_coverage_pct']:>5.1f}% | "
            f"{r['metrics']['total_entries']:>7} | {tpe:>9.1f} | {time_str}"
        )
    print(sep)


def generate_report(all_results: list, gold: dict, paper_stem: str):
    """生成 Markdown 报告"""
    gold_concepts = gold.get("concepts", [])
    gold_methods = gold.get("methods", [])
    gold_rels = gold.get("relations", [])
    gold_type_counts = {
        "concept": len(gold_concepts),
        "method": len(gold_methods),
        "relation": len(gold_rels),
        "experiment": len(gold.get("experiments", [])),
        "dataset": len(gold.get("datasets", [])),
        "conclusion": len(gold.get("conclusions", [])),
        "claim": len(gold.get("claims", [])),
        "future_work": len(gold.get("future_works", [])),
        "limitation": len(gold.get("limitations", [])),
        "performance_result": len(gold.get("performance_results", [])),
    }

    lines = []
    lines.append("# LLM 知识抽取模型评估报告\n")
    lines.append(f"生成时间: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}\n")

    # ── 1. 测试设置 ──
    lines.append("## 1. 测试设置\n")
    lines.append(f"- **论文**: {paper_stem}.md")
    lines.append(f"- **Gold Standard**: {len(gold_concepts)} concepts, {len(gold_methods)} methods, {len(gold_rels)} relations")
    lines.append(f"- **评估模型数**: {len(all_results)}")
    lines.append(f"- **评估维度**: Concept F1, Method F1, Relation F1, 类型覆盖度, Token 效率, Evidence 简洁度\n")

    lines.append("### Gold Standard 标注统计\n")
    lines.append("| 知识类型 | 标注数量 |")
    lines.append("|---------|---------|")
    for t in ALL_TYPES:
        lines.append(f"| {t} | {gold_type_counts.get(t, 0)} |")
    lines.append("")

    # ── 2. 综合排名 ──
    lines.append("## 2. 综合排名\n")
    lines.append("综合得分 = 35%×Concept F1 + 25%×Method F1 + 15%×类型覆盖 + 5%×学科匹配 + 10%×Token效率 + 10%×Evidence简洁度\n")
    lines.append("| 排名 | 模型 | 综合得分 | Concept F1 | Method F1 | 类型覆盖 | 总条目 | Tokens/条 | 耗时 |")
    lines.append("|-----|------|---------|-----------|----------|---------|-------|----------|-----|")
    for i, r in enumerate(all_results, 1):
        tpe = r["metrics"].get("tokens_per_entry", 0)
        time_val = r.get("time", 0)
        time_str = f"{time_val:.1f}s" if time_val > 0 else "-"
        lines.append(
            f"| {i} | {r['model']} | {r['score']:.1f} | "
            f"{r['metrics']['concept_f1']:.3f} | {r['metrics']['method_f1']:.3f} | "
            f"{r['metrics']['type_coverage_pct']:.1f}% | "
            f"{r['metrics']['total_entries']} | {tpe:.1f} | {time_str} |"
        )
    lines.append("")

    # ── 3. 各类型 F1 详情 ──
    lines.append("## 3. 各类型 F1 对比\n")
    lines.append("| 模型 | Concept P/R/F1 | Method P/R/F1 |")
    lines.append("|-----|---------------|--------------|")
    for r in all_results:
        m = r["metrics"]
        lines.append(
            f"| {r['model']} | "
            f"{m['concept_precision']:.2f}/{m['concept_recall']:.2f}/{m['concept_f1']:.2f} | "
            f"{m['method_precision']:.2f}/{m['method_recall']:.2f}/{m['method_f1']:.2f} |"
        )
    lines.append("")
    lines.append("**注**: 所有模型的 Relation F1 均为 0，因为当前 prompt 下无模型输出 relation 类型。")

    # ── 4. 类型分布对比 ──
    lines.append("## 4. 各模型知识类型分布\n")
    type_header = "| 模型 |"
    type_sep = "|-----|"
    for t in ALL_TYPES:
        type_header += f" {t[:6]} |"
        type_sep += "----|"
    lines.append(type_header)
    lines.append(type_sep)
    for r in all_results:
        row = f"| {r['model']} |"
        for t in ALL_TYPES:
            row += f" {r['metrics']['type_counts'].get(t, 0):>4} |"
        lines.append(row)
    lines.append("")

    # ── 5. 概念命中详情 ──
    lines.append("## 5. Top 3 模型概念命中详情\n")
    for r in all_results[:3]:
        m = r["metrics"]
        lines.append(f"### {r['model']} (Concept F1={m['concept_f1']:.3f})\n")
        # 需要重新计算 TP/FP/FN
        entries = r.get("_entries_raw", [])
        pred_concepts = {normalize_term(e["term"]) for e in entries if e["type"] == "concept"}
        gold_concept_norm = {normalize_term(c["term"]) for c in gold_concepts}
        tp = sorted(gold_concept_norm & pred_concepts)
        fp = sorted(pred_concepts - gold_concept_norm)
        fn = sorted(gold_concept_norm - pred_concepts)
        if tp:
            lines.append(f"**命中 ({len(tp)})**: {', '.join(tp)}")
        if fp:
            lines.append(f"**误报 ({len(fp)})**: {', '.join(fp)}")
        if fn:
            lines.append(f"**漏报 ({len(fn)})**: {', '.join(fn)}")
        lines.append("")

    # ── 6. Token 效率 ──
    lines.append("## 6. Token 效率分析\n")
    lines.append("| 模型 | 输出 Tokens | 条目数 | Tokens/条目 | 评估 |")
    lines.append("|-----|-----------|-------|-----------|-----|")
    for r in all_results:
        tpe = r["metrics"].get("tokens_per_entry", 0)
        if tpe == 0:
            rating = "-"
        elif tpe < 200:
            rating = "高效"
        elif tpe < 350:
            rating = "中等"
        else:
            rating = "冗余"
        lines.append(
            f"| {r['model']} | {r['metrics']['completion_tokens']} | "
            f"{r['metrics']['total_entries']} | {tpe:.1f} | {rating} |"
        )
    lines.append("")

    # ── 7. 成本估算 ──
    lines.append("## 7. 大规模成本估算\n")
    lines.append("假设: 每百万 tokens = ¥1 元，处理 8000 万篇论文\n")
    lines.append("| 模型 | 单篇输入 Tokens | 单篇输出 Tokens | 单篇成本(元) | 8000万篇总成本(万元) |")
    lines.append("|-----|---------------|---------------|------------|-------------------|")
    for r in all_results:
        pt = r["metrics"].get("prompt_tokens", 0) or r.get("prompt_tokens", 0)
        ct = r["metrics"].get("completion_tokens", 0)
        total = pt + ct
        cost_per_paper = total / 1_000_000
        total_cost_80m = cost_per_paper * 80_000_000 / 10_000  # in 万元
        lines.append(
            f"| {r['model']} | {pt:,} | {ct:,} | "
            f"¥{cost_per_paper:.4f} | ¥{total_cost_80m:,.0f} |"
        )
    lines.append("")

    # ── 8. 推荐 ──
    lines.append("## 8. 推荐\n")
    best = all_results[0]
    lines.append(f"**综合最佳**: {best['model']} (得分 {best['score']:.1f})")
    lines.append(f"- Concept F1: {best['metrics']['concept_f1']:.3f}")
    lines.append(f"- Method F1: {best['metrics']['method_f1']:.3f}")
    lines.append(f"- 类型覆盖: {best['metrics']['type_coverage_pct']:.1f}%")
    lines.append(f"- Token 效率: {best['metrics'].get('tokens_per_entry', 0):.1f} tokens/条目")

    # 找性价比最好的
    efficient = min(
        [r for r in all_results if r["metrics"].get("tokens_per_entry", 0) > 0],
        key=lambda r: r["metrics"].get("tokens_per_entry", 999) / max(r["score"], 1)
    )
    lines.append(f"\n**性价比最佳**: {efficient['model']} (得分 {efficient['score']:.1f}, {efficient['metrics'].get('tokens_per_entry', 0):.1f} tokens/条目)")

    lines.append("")
    return "\n".join(lines)


def main():
    # 解析参数
    paper_stem = None
    gold_file = None
    i = 1
    while i < len(sys.argv):
        a = sys.argv[i]
        if a == "--paper" and i + 1 < len(sys.argv):
            paper_stem = sys.argv[i + 1]; i += 2; continue
        elif a == "--gold" and i + 1 < len(sys.argv):
            gold_file = sys.argv[i + 1]; i += 2; continue
        i += 1

    if not paper_stem:
        # 优先选择有 gold standard 对应的论文
        gold_files = sorted(GOLD_DIR.glob("gold_*.json"))
        for gf in gold_files:
            # gold_xxx-main.json → paper_stem = xxx-main
            candidate_stem = gf.stem[len("gold_"):]
            # 检查有多少模型有这个 stem 的输出
            count = 0
            for md2 in sorted(TEST_DIR.iterdir()):
                if md2.is_dir() and (md2 / f"{candidate_stem}.json").exists():
                    count += 1
            if count > 0:
                paper_stem = candidate_stem
                break

        if not paper_stem:
            # 如果没有 gold standard 匹配，选有最多模型输出的论文
            max_count = 0
            best_stem = None
            for model_dir in sorted(TEST_DIR.iterdir()):
                if not model_dir.is_dir():
                    continue
                for fpath in sorted(model_dir.glob("*.json")):
                    if fpath.name in ("eval_results.json", "results.json"):
                        continue
                    stem = fpath.stem
                    count = 0
                    for md2 in sorted(TEST_DIR.iterdir()):
                        if md2.is_dir() and (md2 / fpath.name).exists():
                            count += 1
                    if count > max_count:
                        max_count = count
                        best_stem = stem
            paper_stem = best_stem

        if not paper_stem:
            print("错误: 未找到匹配的论文输出文件")
            return
        print(f"自动选择论文: {paper_stem}")

    # 加载 gold standard
    if gold_file:
        gold = json.loads(Path(gold_file).read_text(encoding="utf-8"))
    else:
        gold = load_gold(paper_stem)

    # 收集模型输出
    model_outputs = extract_model_outputs(TEST_DIR, paper_stem)
    if not model_outputs:
        print(f"错误: 未找到 {paper_stem} 的模型输出")
        return
    print(f"找到 {len(model_outputs)} 个模型的输出\n")

    # 获取 token 统计
    token_stats = get_tokens_from_results_json(paper_stem)

    # 评估每个模型
    all_results = []
    for model_name, data in model_outputs.items():
        entries = data["entries"]
        timing = token_stats.get(model_name, {})
        metrics = eval_one_model(entries, gold, timing)

        # 补充 token 信息
        if model_name in token_stats:
            ts = token_stats[model_name]
            metrics["prompt_tokens"] = ts.get("prompt_tokens", metrics.get("prompt_tokens", 0))
            if metrics.get("completion_tokens", 0) == 0:
                metrics["completion_tokens"] = ts.get("completion_tokens", 0)

        score = compute_composite_score(metrics, gold)
        all_results.append({
            "model": model_name,
            "score": score,
            "metrics": metrics,
            "time": timing.get("total_time", 0),
            "_entries_raw": entries,
        })

    # 按综合得分排序
    all_results.sort(key=lambda x: -x["score"])

    # 打印排名
    print_ranking_table(all_results, gold)

    # 保存 JSON
    eval_results = []
    for r in all_results:
        m = r["metrics"]
        eval_results.append({
            "model": r["model"],
            "composite_score": r["score"],
            "concept": {"precision": m["concept_precision"], "recall": m["concept_recall"], "f1": m["concept_f1"], "tp": m["concept_tp"], "fp": m["concept_fp"], "fn": m["concept_fn"]},
            "method": {"precision": m["method_precision"], "recall": m["method_recall"], "f1": m["method_f1"], "tp": m["method_tp"], "fp": m["method_fp"], "fn": m["method_fn"]},
            "relation": {"precision": m["relation_precision"], "recall": m["relation_recall"], "f1": m["relation_f1"]},
            "type_coverage": m["type_coverage_pct"],
            "total_entries": m["total_entries"],
            "type_counts": m["type_counts"],
            "tokens_per_entry": m.get("tokens_per_entry", 0),
            "completion_tokens": m.get("completion_tokens", 0),
        })
    eval_path = TEST_DIR / "eval_results.json"
    eval_path.write_text(json.dumps(eval_results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n详细结果已保存到 {eval_path.name}")

    # 生成报告
    report = generate_report(all_results, gold, paper_stem)
    report_path = TEST_DIR / "eval_report.md"
    report_path.write_text(report, encoding="utf-8")
    print(f"评估报告已保存到 {report_path.name}")


if __name__ == "__main__":
    main()
