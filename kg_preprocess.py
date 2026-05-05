"""
kg_preprocess.py — 论文预处理：正则提取 metadata → LLM 修正 + 学科分类

输入: markdown/*.md
输出: kg_output/*.json (只有 metadata，entries 为空，供 kg_extract.py 补充 entries)

用法:
    python kg_preprocess.py                    # 处理所有 MD
    python kg_preprocess.py paper.md           # 指定文件
    python kg_preprocess.py --force            # 强制重新处理
    python kg_preprocess.py --stream           # 实时显示 LLM 输出
"""

import json
import sys
import random
import logging
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from kg_extract import load_config, generate_doc_id, parse_md_metadata, call_llm, MARKDOWN_DIR, OUTPUT_DIR
from kg_schema import LLMDisciplineResponse
from kg_prompts import build_discipline_prompt

load_dotenv()

BASE_DIR = Path(__file__).parent


def process_one(md_path: Path, client: OpenAI, model: str, cfg: dict, force: bool, stream: bool) -> bool:
    out_path = OUTPUT_DIR / f"{md_path.stem}.json"
    if out_path.exists() and not force:
        print(f"[跳过] {md_path.name}")
        return False

    print(f"[处理] {md_path.name}")
    raw_text = md_path.read_text(encoding="utf-8")

    # Step 1: 正则提取 metadata（兜底）
    md_meta = parse_md_metadata(raw_text, md_path)
    abstract = md_meta.get("abstract") or ""
    introduction = md_meta.get("introduction") or ""
    paper_head = raw_text[:cfg["metadata_head_chars"]]

    # Step 2: 构建 prompt — 优先 abstract+intro，缺失则用前 N 字符
    sys_prompt, user_prompt = build_discipline_prompt(
        abstract, introduction, paper_head,
        regex_title=md_meta.get("title", ""),
        regex_year=md_meta.get("year"),
        regex_doi=md_meta.get("doi", ""),
    )

    # Step 3: 调 LLM — 修正 metadata + 学科分类
    print(f"  调用 LLM 修正元数据+学科分类 ({model})...")
    llm_parsed, _, usage = call_llm(
        client, model, sys_prompt, user_prompt, cfg["temperature"],
        stream=stream, max_tokens=cfg.get("max_output_tokens", 16384),
        max_retries=cfg.get("max_retries", 5))

    if isinstance(llm_parsed.get("secondary_disciplines"), dict):
        llm_parsed["secondary_disciplines"] = [llm_parsed["secondary_disciplines"]]

    try:
        discipline = LLMDisciplineResponse(**llm_parsed).model_dump()
    except Exception:
        discipline = llm_parsed

    # Step 4: LLM 返回值覆盖正则结果
    if discipline.get("title"):
        md_meta["title"] = discipline["title"]
    if discipline.get("year"):
        md_meta["year"] = discipline["year"]
    if discipline.get("doi"):
        md_meta["doi"] = discipline["doi"]

    doc_id = generate_doc_id(md_meta.get("title"), md_path.stem)

    # Step 5: 写出（只有 metadata，entries 为空）
    result = {
        "metadata": {
            "doc_id": doc_id,
            "source_file": md_path.name,
            "title": md_meta["title"],
            "year": md_meta["year"],
            "doi": md_meta["doi"],
            "abstract": abstract,
            "introduction": introduction,
            "primary_discipline": discipline.get("primary_discipline", {}),
            "secondary_disciplines": discipline.get("secondary_disciplines"),
            "keywords": md_meta.get("_keywords_from_paper") or discipline.get("keywords", []),
        },
        "entries": [],
    }
    out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  → {out_path.name}\n")
    return True, usage


def collect_md_files(args: list[str]) -> list[Path]:
    if args:
        files = []
        for name in args:
            p = Path(name)
            if not p.is_absolute():
                if (MARKDOWN_DIR / p).exists():
                    p = MARKDOWN_DIR / p
                elif not p.exists():
                    print(f"不存在: {name}")
                    continue
            files.extend(sorted(p.glob("**/*.md")) if p.is_dir() else [p] if p.is_file() else [])
        return files
    return sorted(MARKDOWN_DIR.glob("**/*.md"))


def main():
    logging.basicConfig(level=logging.WARNING, format="%(asctime)s %(levelname)s %(message)s")
    OUTPUT_DIR.mkdir(exist_ok=True)
    cfg = load_config()
    if not cfg["api_key"]:
        print("错误: 未设置 OPENAI_API_KEY")
        return

    client = OpenAI(api_key=cfg["api_key"], base_url=cfg["base_url"] or None)
    force = "--force" in sys.argv
    stream = "--stream" in sys.argv
    reset_failed = "--reset-failed" in sys.argv

    limit = None
    if "--limit" in sys.argv:
        idx = sys.argv.index("--limit")
        if idx + 1 < len(sys.argv):
            limit = int(sys.argv[idx + 1])
    elif cfg.get("process_limit"):
        limit = cfg["process_limit"]

    skip_next = False
    args = []
    for a in sys.argv[1:]:
        if skip_next:
            skip_next = False
            continue
        if a == "--limit":
            skip_next = True
            continue
        if not a.startswith("--"):
            args.append(a)

    workers = cfg["workers"]
    if workers > 1 and stream:
        print("⚠ 并发模式下自动关闭 --stream")
        stream = False

    md_files = collect_md_files(args)
    if not md_files:
        print("没有找到 MD 文件")
        return

    # 初始化状态库
    from kg_state import StateDB
    db = StateDB()
    if reset_failed:
        db.reset_failed("preprocess")

    # stem_to_path 包含所有目标目录的 MD 文件，不受 limit 裁剪
    stem_to_path = {p.stem: p for p in md_files}
    db.register_files(list(stem_to_path.keys()))
    db.print_stats()

    # limit 用计数器控制，不裁剪文件列表
    if limit:
        print(f"本次最多处理 {limit} 篇")
    done_count = 0
    done_lock = threading.Lock()

    def _worker():
        nonlocal done_count
        while True:
            # 检查是否已达 limit
            if limit:
                with done_lock:
                    if done_count >= limit:
                        break

            stem = db.claim_one("preprocess")
            if stem is None:
                break

            md_path = stem_to_path.get(stem)
            if md_path is None:
                # 不属于本次处理目录，放回 pending，继续找下一个
                db.release(stem, "preprocess")
                continue

            # force 模式：直接处理；非 force：若已有输出则跳过
            out_path = OUTPUT_DIR / f"{stem}.json"
            if out_path.exists() and not force:
                import json as _json
                existing = _json.loads(out_path.read_text(encoding="utf-8"))
                if existing.get("metadata"):
                    db.mark_done(stem, "preprocess")
                    with done_lock:
                        done_count += 1
                    print(f"[已完成] {stem}")
                    continue

            try:
                result = process_one(md_path, client, cfg["model"], cfg, force=True, stream=stream)
                ok = result[0] if isinstance(result, tuple) else result
                usage = result[1] if isinstance(result, tuple) else {}
                if ok:
                    db.mark_done(stem, "preprocess")
                    db.set_preprocess_tokens(stem,
                        prompt_tokens=usage.get("prompt_tokens", 0),
                        completion_tokens=usage.get("completion_tokens", 0))
                    with done_lock:
                        done_count += 1
                    print(f"  ✓ {stem}")
                else:
                    db.mark_failed(stem, "preprocess", "process_one 返回 False")
            except Exception as e:
                db.mark_failed(stem, "preprocess", str(e))
                print(f"  ✗ {stem}: {e}")

    if workers == 1:
        _worker()
    else:
        print(f"并发模式: {workers} 个工作线程\n")
        with ThreadPoolExecutor(max_workers=workers) as pool:
            futures = [pool.submit(_worker) for _ in range(workers)]
            for f in as_completed(futures):
                if f.exception():
                    print(f"工作线程异常: {f.exception()}")

    db.print_stats()


if __name__ == "__main__":
    main()
