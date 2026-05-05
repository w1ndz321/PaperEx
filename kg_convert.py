"""
kg_convert.py — 将 PDF 转换为 Markdown

用法:
    python kg_convert.py                        # 转换 papers/ 下所有 PDF
    python kg_convert.py --input-dir DIR        # 转换指定目录
    python kg_convert.py --backend pymupdf      # 使用 pymupdf 解析 (默认 pymupdf4llm)
    python kg_convert.py --force                # 强制重转
    python kg_convert.py --time                 # 显示耗时
"""

import hashlib
import os
import re
import sys
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
load_dotenv()

BASE_DIR = Path(__file__).parent
PAPERS_DIR = BASE_DIR / "papers"
MARKDOWN_DIR = BASE_DIR / "markdown"


def convert_pdf_to_md(pdf_path: Path, backend: str = "pymupdf4llm") -> tuple[str, float]:
    t0 = time.time()
    if backend == "pymupdf":
        import fitz
        doc = fitz.open(str(pdf_path))
        md_text: str = "\n\n".join(str(page.get_text("text")) for page in doc)
        doc.close()
    else:
        import pymupdf4llm
        md_text = str(pymupdf4llm.to_markdown(str(pdf_path)))
    return md_text, time.time() - t0


def _clean_md(md_text: str) -> str:
    md_text = re.sub(r"\*\*==> picture \[.*?\] intentionally omitted <==\*\*\n?", "", md_text)
    md_text = re.sub(r"(?m)^\|.*\n?", "", md_text)
    # 截掉 References/Bibliography/参考文献 之后的内容
    m = re.search(r"\n#{1,2}\s+\*?\*?(References|Bibliography|参考文献)\*?\*?\s*", md_text, re.IGNORECASE)
    if m:
        md_text = md_text[:m.start()]
    return md_text


def _fix_abstract_order(md_text: str) -> str:
    pattern = r"(##\s+\*?\*?Abstract\*?\*?\s*\n)(.*?)(?=\n##|\Z)"
    match = re.search(pattern, md_text, re.DOTALL | re.IGNORECASE)
    if not match:
        return md_text
    heading = match.group(1)
    body = match.group(2).strip()
    paragraphs = [p.strip() for p in body.split("\n\n") if p.strip()]
    if len(paragraphs) < 2 or not paragraphs[0][0].islower():
        return md_text
    paragraphs = paragraphs[1:] + [paragraphs[0]]
    merged = [paragraphs[0]]
    for p in paragraphs[1:]:
        if p[0].islower():
            merged[-1] += " " + p
        else:
            merged.append(p)
    return md_text[:match.start()] + heading + "\n\n".join(merged) + md_text[match.end():]


def collect_pdfs(args: list[str], input_dir: Optional[Path] = None) -> list[Path]:
    pdfs = []
    if input_dir:
        return sorted(input_dir.glob("**/*.pdf"))
    if args:
        for name in args:
            p = Path(name)
            if not p.is_absolute():
                if (PAPERS_DIR / p).exists():
                    p = PAPERS_DIR / p
                elif not p.exists():
                    print(f"不存在: {name}")
                    continue
            pdfs.extend(sorted(p.glob("**/*.pdf")) if p.is_dir() else [p] if p.is_file() else [])
    else:
        pdfs = sorted(PAPERS_DIR.glob("**/*.pdf"))
        if not pdfs:
            print("papers/ 目录下没有 PDF 文件")
    return pdfs


def convert_one(pdf_path: Path, input_dir: Optional[Path] = None, backend: str = "pymupdf4llm", force: bool = False) -> tuple[Path, bool, float, int, str]:
    if input_dir:
        md_path = MARKDOWN_DIR / input_dir.name / f"{pdf_path.stem}.md"
    else:
        md_path = MARKDOWN_DIR / f"{pdf_path.stem}.md"
    if md_path.exists() and not force:
        content = md_path.read_text(encoding="utf-8")
        return md_path, True, 0.0, len(content), hashlib.md5(content.encode()).hexdigest()
    md_path.parent.mkdir(parents=True, exist_ok=True)
    print(f"  转换: {pdf_path.name} → {md_path}")
    md_text, elapsed = convert_pdf_to_md(pdf_path, backend)
    md_text = _fix_abstract_order(_clean_md(md_text))
    md_path.write_text(md_text, encoding="utf-8")
    content_hash = hashlib.md5(md_text.encode()).hexdigest()
    print(f"  完成: {len(md_text)} 字符, 耗时 {elapsed:.2f}s")
    return md_path, False, elapsed, len(md_text), content_hash


def main():
    MARKDOWN_DIR.mkdir(exist_ok=True)
    force = "--force" in sys.argv
    show_time = "--time" in sys.argv
    workers = int(os.environ.get("WORKERS", "1"))

    backend = "pymupdf4llm"
    if "--backend" in sys.argv:
        idx = sys.argv.index("--backend")
        if idx + 1 < len(sys.argv):
            backend = sys.argv[idx + 1]

    input_dir = None
    if "--input-dir" in sys.argv:
        idx = sys.argv.index("--input-dir")
        if idx + 1 < len(sys.argv):
            input_dir = Path(sys.argv[idx + 1])
            if not input_dir.is_dir():
                print(f"目录不存在: {input_dir}")
                return
    args = [a for a in sys.argv[1:] if not a.startswith("--")]

    pdfs = collect_pdfs(args, input_dir)
    if not pdfs:
        return

    # 初始化状态库
    from kg_state import StateDB
    db = StateDB()
    db.register_files([p.stem for p in pdfs])

    min_md_chars = int(os.environ.get("MIN_MD_CHARS", "10000"))
    t0 = time.time()
    stats_lock = threading.Lock()
    total_parse = 0.0
    converted = 0
    skipped = 0
    time_records = []
    total = len(pdfs)
    print(f"共 {total} 个文件，{workers} 个线程\n")

    def _process(pdf):
        nonlocal total_parse, converted, skipped
        stem = pdf.stem
        try:
            _, was_skip, elapsed, char_count, content_hash = convert_one(pdf, input_dir, backend, force)

            # 哈希去重：检查是否与已有文件内容相同
            dup_of = db.check_and_set_hash(stem, content_hash)
            db.mark_done(stem, "convert")
            if char_count:
                db.set_char_count(stem, char_count)
            if dup_of:
                db.skip(stem, f"内容与 {dup_of} 重复")
                print(f"  [重复] {pdf.name} 与 {dup_of} 内容相同，跳过")
                with stats_lock:
                    skipped += 1
                return

            # 字符数不足：标记 skip，preprocess/extract 不处理
            if char_count < min_md_chars:
                db.skip(stem, f"字符数不足: {char_count} < {min_md_chars}")
                print(f"  [跳过] {pdf.name}  ({char_count} 字符)")
            with stats_lock:
                if was_skip:
                    skipped += 1
                else:
                    total_parse += elapsed
                    converted += 1
                    time_records.append((pdf.name, elapsed))
        except Exception as e:
            db.mark_failed(stem, "convert", str(e))
            print(f"  ✗ {pdf.name}: {e}")

    if workers == 1:
        for i, pdf in enumerate(pdfs, 1):
            print(f"[{i}/{total}]", end=" ")
            _process(pdf)
    else:
        with ThreadPoolExecutor(max_workers=workers) as pool:
            futures = {pool.submit(_process, pdf): pdf for pdf in pdfs}
            done = 0
            for f in as_completed(futures):
                done += 1
                if done % 100 == 0:
                    print(f"  进度: {done}/{total}")
                if f.exception():
                    print(f"  ✗ 线程异常: {f.exception()}")

    print(f"\n{'='*50}")
    print(f"总耗时: {time.time()-t0:.2f}s | 转换: {converted} | 跳过: {skipped}")
    if converted:
        print(f"纯解析耗时: {total_parse:.2f}s (平均 {total_parse/converted:.2f}s/文件)")
        if show_time:
            for name, t in sorted(time_records, key=lambda x: -x[1]):
                print(f"  {name}: {t:.2f}s")
    print(f"{'='*50}\n全部完成。")
    db.print_stats()


if __name__ == "__main__":
    main()
