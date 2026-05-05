"""
llm_test.py — 测试不同 LLM 模型在知识抽取上的表现

对比流程和 kg_preprocess + kg_extract 一致：
  Step 1: 学科分类 + metadata 修正（轻量 LLM）
  Step 2: 知识抽取（重量 LLM）

用法:
    python llm_test.py                        # 测试所有模型
    python llm_test.py --paper paper.md       # 指定论文
    python llm_test.py --task discipline      # 只测试学科推断
    python llm_test.py --task extraction      # 只测试知识抽取
    python llm_test.py --stream               # 实时显示 LLM 输出
"""

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from kg_extract import (
    call_llm,
    load_config,
    parse_md_metadata,
    generate_doc_id,
    build_output,
    load_meta,
    MARKDOWN_DIR,
)
from kg_prompts import build_discipline_prompt, build_extraction_prompt
from kg_schema import LLMDisciplineResponse, LLMExtractionResponse

load_dotenv()

MODELS = [
    "gpt-4o",
    "gpt-4o-mini",
    "gpt-oss-120b",
    "gpt-5-mini",
    "gpt-5-nano",
    "deepseek-chat",
    "deepseek-v3",
    "deepseek-v3.1",
    "deepseek-v3.2",
    # "gemini-2.0-flash",
    # "gemini-2.0-flash-lite",
    "gemini-2.5-flash",
    # "gemini-2.5-flash-lite",
    "gemini-2.5-flash-nothinking",
    "qwen3-235b-a22b",
]

BASE_DIR = Path(__file__).parent
TEST_DIR = BASE_DIR / "llm_test"


def run_full_pipeline(client, model, md_path, cfg, stream=False, task_filter=None):
    """运行完整抽取流程（和 preprocess + extract 一致）"""
    full_text = md_path.read_text(encoding="utf-8")
    md_meta = parse_md_metadata(full_text, md_path)
    abstract = md_meta.get("abstract") or ""
    introduction = md_meta.get("introduction") or ""
    paper_head = full_text[:cfg.get("metadata_head_chars", 3000)]

    discipline_parsed = {}
    extraction_parsed = {}
    timing = {}

    # Step 1: 学科分类 + metadata 修正
    if task_filter in (None, "discipline"):
        sys_d, user_d = build_discipline_prompt(
            abstract, introduction, paper_head,
            regex_title=md_meta.get("title", ""),
            regex_year=md_meta.get("year"),
            regex_doi=md_meta.get("doi", ""),
        )
        t0 = time.time()
        dp, _, du = call_llm(client, model, sys_d, user_d, cfg["temperature"], stream=stream, max_tokens=cfg.get("max_output_tokens", 16384))
        timing["discipline"] = {"total_time": time.time() - t0, "prompt_tokens": du.get("prompt_tokens", 0), "completion_tokens": du.get("completion_tokens", 0)}
        if not isinstance(dp, dict): dp = {}
        try: discipline_parsed = LLMDisciplineResponse(**dp).model_dump()
        except Exception: discipline_parsed = dp

        # LLM 修正覆盖正则
        if discipline_parsed.get("title"):
            md_meta["title"] = discipline_parsed["title"]
        if discipline_parsed.get("year"):
            md_meta["year"] = discipline_parsed["year"]
        if discipline_parsed.get("doi"):
            md_meta["doi"] = discipline_parsed["doi"]

    # 组装 metadata（供 build_output 使用）
    meta_for_output = {
        "title": md_meta.get("title"),
        "year": md_meta.get("year"),
        "doi": md_meta.get("doi"),
        "abstract": abstract,
        "introduction": introduction,
        "keywords": md_meta.get("_keywords_from_paper") or discipline_parsed.get("keywords", []),
        "primary_discipline": discipline_parsed.get("primary_discipline", {}),
        "secondary_disciplines": discipline_parsed.get("secondary_disciplines"),
    }

    # Step 2: 知识抽取
    if task_filter in (None, "extraction"):
        max_chars = cfg["max_input_chars"]
        text = full_text[:max_chars]
        sys_e, user_e = build_extraction_prompt(text)
        t0 = time.time()
        kp, _, ku = call_llm(client, model, sys_e, user_e, cfg["temperature"], stream=stream, max_tokens=cfg.get("max_output_tokens", 16384))
        timing["extraction"] = {"total_time": time.time() - t0, "prompt_tokens": ku.get("prompt_tokens", 0), "completion_tokens": ku.get("completion_tokens", 0)}
        if not isinstance(kp, dict): kp = {}
        try: extraction_parsed = LLMExtractionResponse(**kp).model_dump()
        except Exception: extraction_parsed = kp

    doc_id = generate_doc_id(md_meta.get("title"), md_path.stem)
    result = build_output(meta_for_output, extraction_parsed, doc_id, model)
    result["test_info"] = {"model": model, "test_timestamp": datetime.now(timezone.utc).isoformat()}
    entries = len(result.get("entries", []))
    return result, timing, entries


def print_table(results):
    header = f"{'模型':<25} | {'输入':>6} | {'输出':>6} | {'总耗时':>8} | {'条目数':>5}"
    sep = "-" * len(header)
    print(sep)
    print(header)
    print(sep)
    for r in results:
        pt = r["prompt_tokens"]
        ct = r["completion_tokens"]
        t = f'{r["total_time"]:.1f}s'
        entries = r.get("entries", "-")
        print(f"{r['model']:<25} | {pt:>6} | {ct:>6} | {t:>8} | {entries:>5}")
    print(sep)


def main():
    cfg = load_config()
    if not cfg["api_key"]:
        print("错误: 未设置 OPENAI_API_KEY")
        return

    task_filter = None
    paper_args = []
    stream = "--stream" in sys.argv
    i = 1
    while i < len(sys.argv):
        a = sys.argv[i]
        if a == "--task" and i + 1 < len(sys.argv):
            task_filter = sys.argv[i + 1]; i += 2; continue
        elif a == "--paper" and i + 1 < len(sys.argv):
            paper_args.append(sys.argv[i + 1]); i += 2; continue
        i += 1

    files = sorted(MARKDOWN_DIR.glob("*.md")) if not paper_args else []
    if paper_args:
        for name in paper_args:
            p = Path(name)
            if not p.is_absolute(): p = MARKDOWN_DIR / p
            if p.is_file(): files.append(p)
            elif p.is_dir(): files.extend(sorted(p.glob("*.md")))
    if not files:
        print("没有找到 MD 文件")
        return
    print(f"测试论文: {', '.join(f.name for f in files)}\n")

    client = OpenAI(api_key=cfg["api_key"], base_url=cfg["base_url"] or None)
    summary_results = []

    for model in MODELS:
        model_dir = TEST_DIR / model
        model_dir.mkdir(parents=True, exist_ok=True)
        print(f"\n{'='*50}")
        print(f"测试模型: {model}")
        print(f"{'='*50}")

        total_pt, total_ct, total_time = 0, 0, 0.0
        total_entries = 0

        for md_path in files:
            out_path = model_dir / f"{md_path.stem}.json"
            print(f"\n  [{md_path.name}] ...")
            try:
                result, timing, entries = run_full_pipeline(client, model, md_path, cfg, stream=stream, task_filter=task_filter)
                out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
                print(f"  → 保存到 {model}/{out_path.name} ({entries} 条)")
                for t in timing.values():
                    total_pt += t.get("prompt_tokens", 0)
                    total_ct += t.get("completion_tokens", 0)
                    total_time += t.get("total_time", 0)
                total_entries += entries
            except Exception as e:
                print(f"  ✗ 失败: {e}")
                continue

        summary_results.append({
            "model": model, "papers_tested": len(files),
            "prompt_tokens": total_pt, "completion_tokens": total_ct,
            "total_time": round(total_time, 1), "total_entries": total_entries,
        })

    print(f"\n\n{'='*60}")
    print(f"模型测试报告: {', '.join(f.name for f in files)}")
    print(f"{'='*60}")
    print_table(summary_results)

    results_path = TEST_DIR / "results.json"
    existing = json.loads(results_path.read_text(encoding="utf-8")) if results_path.exists() else {}
    existing.setdefault("papers_tested", [])
    for r in summary_results:
        existing["papers_tested"].append({**r, "paper": [f.name for f in files], "tested_at": datetime.now(timezone.utc).isoformat()})
    seen = {}
    for pt in existing["papers_tested"]:
        key = f"{pt.get('paper', ['unknown'])[0]}__{pt['model']}"
        seen[key] = pt
    existing["papers_tested"] = list(seen.values())
    existing["updated_at"] = datetime.now(timezone.utc).isoformat()
    results_path.write_text(json.dumps(existing, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n汇总结果已保存到 {results_path.name}")


if __name__ == "__main__":
    main()
