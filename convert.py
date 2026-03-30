"""
convert.py — 将 papers/ 中的 PDF 转换为 markdown/ 中的 MD 文件

用法:
    python convert.py                  # 转换 papers/ 下所有 PDF
    python convert.py paper.pdf        # 转换指定文件
    python convert.py --force          # 强制重新转换已有 MD 的文件
"""

import json
import sys
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


def convert_pdf_to_md(pdf_path: Path) -> str:
    """将 PDF 转为 Markdown 字符串"""
    import pymupdf4llm
    md_text = pymupdf4llm.to_markdown(str(pdf_path))
    print(f"  [pymupdf4llm] 转换成功")
    return md_text



def convert_one(pdf_path: Path, force: bool = False) -> tuple[Path, bool]:
    """转换单个 PDF，返回 (输出 MD 路径, 是否跳过)。"""
    md_path = MARKDOWN_DIR / f"{pdf_path.stem}.md"

    if md_path.exists() and not force:
        return md_path, True

    print(f"  转换: {pdf_path.name} → {md_path.name}")
    md_text = convert_pdf_to_md(pdf_path)
    md_path.write_text(md_text, encoding="utf-8")
    update_stats(md_path, len(md_text))
    print(f"  完成: {len(md_text)} 字符")
    return md_path, False


def main():
    MARKDOWN_DIR.mkdir(exist_ok=True)

    force = "--force" in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("--")]

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
            _, was_skipped = convert_one(pdf_path, force=force)
            if was_skipped:
                skipped += 1
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
            _, was_skipped = convert_one(pdf_path, force=force)
            if was_skipped:
                skipped += 1
        if skipped:
            print(f"已跳过 {skipped} 个文件（已存在）")

    print("全部完成。")


if __name__ == "__main__":
    main()
