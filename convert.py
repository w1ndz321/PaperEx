"""
convert.py — 将 papers/ 中的 PDF 转换为 markdown/ 中的 MD 文件

用法:
    python convert.py                  # 转换 papers/ 下所有 PDF
    python convert.py paper.pdf        # 转换指定文件
    python convert.py --force          # 强制重新转换已有 MD 的文件
    python convert.py --time           # 显示详细时间统计
"""

import json
import re
import sys
import time
from pathlib import Path

# 项目根目录
BASE_DIR = Path(__file__).parent
PAPERS_DIR = BASE_DIR / "papers"
MARKDOWN_DIR = BASE_DIR / "markdown"
STATS_PATH = MARKDOWN_DIR / "stats.json"


def update_stats(md_path: Path, char_count: int):
    """更新 markdown/stats.json 中的字符数记录。"""
    stats = {}
    if STATS_PATH.exists():
        stats = json.loads(STATS_PATH.read_text(encoding="utf-8"))
    stats[md_path.name] = char_count
    STATS_PATH.write_text(json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8")


def _clean_md(md_text: str) -> str:
    """去除图片占位符和混乱的表格内容，保留图片中提取出的文字。"""
    # 去除图片占位符行：**==> picture [...] intentionally omitted <==**
    md_text = re.sub(r"\*\*==> picture \[.*?\] intentionally omitted <==\*\*\n?", "", md_text)

    # 去除表格（连续的 | 开头的行）
    md_text = re.sub(r"(?m)^\|.*\n?", "", md_text)

    return md_text


def _fix_abstract_order(md_text: str) -> str:
    """修复双栏 PDF 导致的 abstract 段落错位问题。

    双栏论文转换时，右栏溢出的片段会排到 ## Abstract 之后的第一段，
    表现为第一段首字母小写。处理步骤：
    1. 将首字母小写的第一段移到末尾（还原位置）
    2. 合并所有首字母小写的段落到上一段（还原被截断的句子）
    """
    pattern = r"(##\s+\*?\*?Abstract\*?\*?\s*\n)(.*?)(?=\n##|\Z)"
    match = re.search(pattern, md_text, re.DOTALL | re.IGNORECASE)
    if not match:
        return md_text

    heading = match.group(1)
    body = match.group(2).strip()
    paragraphs = [p.strip() for p in body.split("\n\n") if p.strip()]

    if len(paragraphs) < 2 or not paragraphs[0][0].islower():
        return md_text

    # 步骤1：首段小写，移到末尾
    paragraphs = paragraphs[1:] + [paragraphs[0]]

    # 步骤2：将仍以小写开头的段落合并到上一段
    merged = [paragraphs[0]]
    for p in paragraphs[1:]:
        if p[0].islower():
            merged[-1] = merged[-1] + " " + p
        else:
            merged.append(p)

    fixed_body = "\n\n".join(merged)
    md_text = md_text[:match.start()] + heading + fixed_body + md_text[match.end():]
    return md_text


def convert_pdf_to_md(pdf_path: Path) -> tuple[str, float]:
    """将 PDF 转为 Markdown 字符串，返回 (markdown文本, 耗时秒数)"""
    import pymupdf4llm
    start_time = time.time()
    md_text = pymupdf4llm.to_markdown(str(pdf_path))
    elapsed = time.time() - start_time
    print(f"  [pymupdf4llm] 转换成功，耗时 {elapsed:.2f}s")
    return md_text, elapsed



def convert_one(pdf_path: Path, force: bool = False) -> tuple[Path, bool, float]:
    """转换单个 PDF，返回 (输出 MD 路径, 是否跳过, 耗时秒数)。"""
    md_path = MARKDOWN_DIR / f"{pdf_path.stem}.md"

    if md_path.exists() and not force:
        return md_path, True, 0.0

    print(f"  转换: {pdf_path.name} → {md_path.name}")
    md_text, elapsed = convert_pdf_to_md(pdf_path)
    md_text = _clean_md(md_text)
    md_text = _fix_abstract_order(md_text)
    md_path.write_text(md_text, encoding="utf-8")
    update_stats(md_path, len(md_text))
    print(f"  完成: {len(md_text)} 字符")
    return md_path, False, elapsed


def main():
    MARKDOWN_DIR.mkdir(exist_ok=True)

    force = "--force" in sys.argv
    show_time = "--time" in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("--")]

    # 时间统计
    total_start = time.time()
    total_parse_time = 0.0
    converted_count = 0
    time_records = []  # 记录每个文件的时间

    if args:
        # 转换指定文件
        skipped = 0
        for name in args:
            pdf_path = Path(name)
            if not pdf_path.is_absolute():
                pdf_path = PAPERS_DIR / name
            if not pdf_path.exists():
                print(f"文件不存在: {pdf_path}")
                continue
            _, was_skipped, elapsed = convert_one(pdf_path, force=force)
            if was_skipped:
                skipped += 1
            else:
                total_parse_time += elapsed
                converted_count += 1
                time_records.append((pdf_path.name, elapsed))
        if skipped:
            print(f"已跳过 {skipped} 个文件（已存在）")
    else:
        # 转换 papers/ 下所有 PDF
        pdfs = sorted(PAPERS_DIR.glob("*.pdf"))
        if not pdfs:
            print(f"papers/ 目录下没有 PDF 文件")
            return
        print(f"找到 {len(pdfs)} 个 PDF 文件")
        skipped = 0
        for pdf_path in pdfs:
            _, was_skipped, elapsed = convert_one(pdf_path, force=force)
            if was_skipped:
                skipped += 1
            else:
                total_parse_time += elapsed
                converted_count += 1
                time_records.append((pdf_path.name, elapsed))
        if skipped:
            print(f"已跳过 {skipped} 个文件（已存在）")

    # 显示时间统计
    total_elapsed = time.time() - total_start
    print("\n" + "=" * 50)
    print("时间统计:")
    print(f"  总耗时: {total_elapsed:.2f}s")
    print(f"  转换文件数: {converted_count}")

    if converted_count > 0:
        print(f"  纯解析耗时: {total_parse_time:.2f}s")
        print(f"  平均每文件: {total_parse_time / converted_count:.2f}s")

        if show_time and time_records:
            print("\n  各文件耗时:")
            for name, t in sorted(time_records, key=lambda x: x[1], reverse=True):
                print(f"    {name}: {t:.2f}s")

    print("=" * 50)
    print("全部完成。")


if __name__ == "__main__":
    main()
