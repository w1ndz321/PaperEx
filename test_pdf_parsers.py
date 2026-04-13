"""
测试5个PDF解析库的效果与时间
"""

import csv
import multiprocessing
import os
import re
import time
from pathlib import Path

PAPERS_DIR = Path("papers")
OUTPUT_DIR = Path("parser_output")
RECORD_FILE = OUTPUT_DIR / "parse_records.csv"
TIMEOUT = 100  # 超时秒数


def run_with_timeout(func, args, timeout):
    """带超时执行函数，返回 (结果, 是否超时或错误信息, 耗时)"""
    start_time = time.time()

    def wrapper(conn):
        try:
            result = func(*args)
            conn.send((result, False))
        except Exception as e:
            conn.send((None, str(e)))
        finally:
            conn.close()

    parent_conn, child_conn = multiprocessing.Pipe()
    p = multiprocessing.Process(target=wrapper, args=(child_conn,))
    p.start()
    p.join(timeout)
    elapsed = time.time() - start_time

    if p.is_alive():
        p.terminate()
        p.join()
        return None, True, elapsed  # 超时

    if parent_conn.poll():
        result, error = parent_conn.recv()
        if error:
            return None, error, elapsed
        return result, False, elapsed
    return None, "无返回结果", elapsed


def get_pdfs():
    """获取papers目录及子目录下所有PDF"""
    return sorted(PAPERS_DIR.rglob("*.pdf"))


def get_page_count(pdf_path: str) -> int:
    """获取PDF页数"""
    try:
        import fitz
        doc = fitz.open(pdf_path)
        count = len(doc)
        doc.close()
        return count
    except:
        return 0


def init_record_file():
    """初始化记录文件"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    if not RECORD_FILE.exists():
        with open(RECORD_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                '文件名', '页数',
                'pypdf_字符数', 'pypdf_时间',
                'pymupdf_字符数', 'pymupdf_时间',
                'pymupdf4llm_字符数', 'pymupdf4llm_时间',
                'pdfplumber_字符数', 'pdfplumber_时间',
                'markitdown_字符数', 'markitdown_时间'
            ])


def save_record(records: dict):
    """保存一条记录"""
    with open(RECORD_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            records['文件名'],
            records['页数'],
            records.get('pypdf_chars', ''),
            records.get('pypdf_time', ''),
            records.get('pymupdf_chars', ''),
            records.get('pymupdf_time', ''),
            records.get('pymupdf4llm_chars', ''),
            records.get('pymupdf4llm_time', ''),
            records.get('pdfplumber_chars', ''),
            records.get('pdfplumber_time', ''),
            records.get('markitdown_chars', ''),
            records.get('markitdown_time', ''),
        ])


def text_to_md(text: str) -> str:
    """纯文本转Markdown"""
    lines = text.split('\n')
    md_lines = []
    for line in lines:
        line = line.strip()
        if not line:
            md_lines.append('')
        elif line.isupper() or re.match(r'^\d+\.?\s+[A-Z]', line):
            md_lines.append(f'## {line}')
        else:
            md_lines.append(line)
    return '\n'.join(md_lines)


def save_file(folder: Path, filename: str, content: str):
    folder.mkdir(parents=True, exist_ok=True)
    (folder / filename).write_text(content, encoding='utf-8')


# ========== 解析函数（返回字符数和时间） ==========

def do_pypdf(pdf_path: str) -> str:
    from pypdf import PdfReader
    reader = PdfReader(pdf_path)
    return '\n\n'.join(page.extract_text() or '' for page in reader.pages)

def do_pymupdf(pdf_path: str) -> str:
    import fitz
    doc = fitz.open(pdf_path)
    text = '\n\n'.join(page.get_text() for page in doc)
    doc.close()
    return text

def do_pymupdf4llm(pdf_path: str) -> str:
    import pymupdf4llm
    return pymupdf4llm.to_markdown(pdf_path)

def do_pdfplumber(pdf_path: str) -> str:
    import pdfplumber
    with pdfplumber.open(pdf_path) as doc:
        return '\n\n'.join(page.extract_text() or '' for page in doc.pages)

def do_markitdown(pdf_path: str, converter) -> str:
    return converter.convert(pdf_path).text_content


def parse_with_pypdf(pdf_path: Path) -> tuple[int, float, str]:
    """pypdf解析，返回(字符数, 时间, 文本)"""
    t1 = time.time()
    text = do_pypdf(str(pdf_path))
    t2 = time.time()
    return len(text), t2 - t1, text

def parse_with_pymupdf(pdf_path: Path) -> tuple[int, float, str]:
    """pymupdf解析"""
    t1 = time.time()
    text = do_pymupdf(str(pdf_path))
    t2 = time.time()
    return len(text), t2 - t1, text

def parse_with_pymupdf4llm(pdf_path: Path) -> tuple[int, float, str]:
    """pymupdf4llm解析"""
    t1 = time.time()
    md = do_pymupdf4llm(str(pdf_path))
    t2 = time.time()
    return len(md), t2 - t1, md

def parse_with_pdfplumber(pdf_path: Path) -> tuple[int, float, str]:
    """pdfplumber解析"""
    t1 = time.time()
    text = do_pdfplumber(str(pdf_path))
    t2 = time.time()
    return len(text), t2 - t1, text

def parse_with_markitdown(pdf_path: Path, converter) -> tuple[int, float, str]:
    """markitdown解析"""
    t1 = time.time()
    md = do_markitdown(str(pdf_path), converter)
    t2 = time.time()
    return len(md), t2 - t1, md


# ========== 带超时的解析 ==========

def parse_pypdf_timeout(pdf_path: Path):
    result, status, elapsed = run_with_timeout(do_pypdf, (str(pdf_path),), TIMEOUT)
    if status is True:
        return None, elapsed, "超时"
    elif isinstance(status, str):
        return None, elapsed, status
    return len(result), elapsed, result

def parse_pymupdf_timeout(pdf_path: Path):
    result, status, elapsed = run_with_timeout(do_pymupdf, (str(pdf_path),), TIMEOUT)
    if status is True:
        return None, elapsed, "超时"
    elif isinstance(status, str):
        return None, elapsed, status
    return len(result), elapsed, result

def parse_pymupdf4llm_timeout(pdf_path: Path):
    result, status, elapsed = run_with_timeout(do_pymupdf4llm, (str(pdf_path),), TIMEOUT)
    if status is True:
        return None, elapsed, "超时"
    elif isinstance(status, str):
        return None, elapsed, status
    return len(result), elapsed, result

def parse_pdfplumber_timeout(pdf_path: Path):
    result, status, elapsed = run_with_timeout(do_pdfplumber, (str(pdf_path),), TIMEOUT)
    if status is True:
        return None, elapsed, "超时"
    elif isinstance(status, str):
        return None, elapsed, status
    return len(result), elapsed, result

def parse_markitdown_timeout(pdf_path: Path, converter):
    result, status, elapsed = run_with_timeout(do_markitdown, (str(pdf_path), converter), TIMEOUT)
    if status is True:
        return None, elapsed, "超时"
    elif isinstance(status, str):
        return None, elapsed, status
    return len(result), elapsed, result


# ========== 主函数 ==========

def main():
    pdfs = get_pdfs()
    print(f"找到 {len(pdfs)} 个PDF文件")
    print("=" * 50)

    init_record_file()

    # 统计每个库的时间 {库名: [时间列表]}
    time_stats = {
        'pypdf': [],
        'pymupdf': [],
        'pymupdf4llm': [],
        'pdfplumber': [],
        'markitdown': []
    }

    # 准备markitdown converter（避免重复初始化）
    markitdown_converter = None
    try:
        from markitdown import MarkItDown
        markitdown_converter = MarkItDown()
    except:
        pass

    for pdf in pdfs:
        print(f"\n处理: {pdf.relative_to(PAPERS_DIR)}")
        records = {
            '文件名': str(pdf.relative_to(PAPERS_DIR)),
            '页数': get_page_count(str(pdf))
        }

        # pypdf
        try:
            chars, t, text = parse_pypdf_timeout(pdf)
            if text == "超时":
                print(f"  [pypdf] 超时! 跳过")
                time_stats['pypdf_timeout'] = time_stats.get('pypdf_timeout', 0) + 1
            elif isinstance(text, str) and text.startswith("Error"):
                print(f"  [pypdf] 错误: {text}")
            else:
                records['pypdf_chars'] = chars
                records['pypdf_time'] = f"{t:.2f}"
                time_stats['pypdf'].append(t)
                save_file(OUTPUT_DIR / "pypdf", f"{pdf.stem}.txt", text)
                save_file(OUTPUT_DIR / "pypdf", f"{pdf.stem}.md", text_to_md(text))
                print(f"  [pypdf] {chars}字符, {t:.2f}s")
        except ImportError:
            print("  [pypdf] 未安装")
        except Exception as e:
            print(f"  [pypdf] 错误: {e}")

        # pymupdf
        try:
            chars, t, text = parse_pymupdf_timeout(pdf)
            if text == "超时":
                print(f"  [pymupdf] 超时! 跳过")
                time_stats['pymupdf_timeout'] = time_stats.get('pymupdf_timeout', 0) + 1
            elif isinstance(text, str) and text.startswith("Error"):
                print(f"  [pymupdf] 错误: {text}")
            else:
                records['pymupdf_chars'] = chars
                records['pymupdf_time'] = f"{t:.2f}"
                time_stats['pymupdf'].append(t)
                save_file(OUTPUT_DIR / "pymupdf", f"{pdf.stem}.txt", text)
                save_file(OUTPUT_DIR / "pymupdf", f"{pdf.stem}.md", text_to_md(text))
                print(f"  [pymupdf] {chars}字符, {t:.2f}s")
        except ImportError:
            print("  [pymupdf] 未安装")
        except Exception as e:
            print(f"  [pymupdf] 错误: {e}")

        # pymupdf4llm
        try:
            chars, t, md = parse_pymupdf4llm_timeout(pdf)
            if md == "超时":
                print(f"  [pymupdf4llm] 超时! 跳过")
                time_stats['pymupdf4llm_timeout'] = time_stats.get('pymupdf4llm_timeout', 0) + 1
            elif isinstance(md, str) and md.startswith("Error"):
                print(f"  [pymupdf4llm] 错误: {md}")
            else:
                records['pymupdf4llm_chars'] = chars
                records['pymupdf4llm_time'] = f"{t:.2f}"
                time_stats['pymupdf4llm'].append(t)
                save_file(OUTPUT_DIR / "pymupdf4llm", f"{pdf.stem}.md", md)
                print(f"  [pymupdf4llm] {chars}字符, {t:.2f}s")
        except ImportError:
            print("  [pymupdf4llm] 未安装")
        except Exception as e:
            print(f"  [pymupdf4llm] 错误: {e}")

        # pdfplumber
        try:
            chars, t, text = parse_pdfplumber_timeout(pdf)
            if text == "超时":
                print(f"  [pdfplumber] 超时! 跳过")
                time_stats['pdfplumber_timeout'] = time_stats.get('pdfplumber_timeout', 0) + 1
            elif isinstance(text, str) and text.startswith("Error"):
                print(f"  [pdfplumber] 错误: {text}")
            else:
                records['pdfplumber_chars'] = chars
                records['pdfplumber_time'] = f"{t:.2f}"
                time_stats['pdfplumber'].append(t)
                save_file(OUTPUT_DIR / "pdfplumber", f"{pdf.stem}.txt", text)
                save_file(OUTPUT_DIR / "pdfplumber", f"{pdf.stem}.md", text_to_md(text))
                print(f"  [pdfplumber] {chars}字符, {t:.2f}s")
        except ImportError:
            print("  [pdfplumber] 未安装")
        except Exception as e:
            print(f"  [pdfplumber] 错误: {e}")

        # markitdown
        if markitdown_converter:
            try:
                chars, t, md = parse_markitdown_timeout(pdf, markitdown_converter)
                if md == "超时":
                    print(f"  [markitdown] 超时! 跳过")
                    time_stats['markitdown_timeout'] = time_stats.get('markitdown_timeout', 0) + 1
                elif isinstance(md, str) and md.startswith("Error"):
                    print(f"  [markitdown] 错误: {md}")
                else:
                    records['markitdown_chars'] = chars
                    records['markitdown_time'] = f"{t:.2f}"
                    time_stats['markitdown'].append(t)
                    save_file(OUTPUT_DIR / "markitdown", f"{pdf.stem}.md", md)
                    print(f"  [markitdown] {chars}字符, {t:.2f}s")
            except Exception as e:
                print(f"  [markitdown] 错误: {e}")
        else:
            print("  [markitdown] 未安装")

        # 保存记录
        save_record(records)

    # 输出统计
    print("\n" + "=" * 50)
    print("统计汇总:")
    print("-" * 50)
    print(f"{'库名':<15} {'成功':<6} {'超时':<6} {'平均时间':<12} {'最长时间':<12}")
    print("-" * 50)
    for lib in ['pypdf', 'pymupdf', 'pymupdf4llm', 'pdfplumber', 'markitdown']:
        times = time_stats.get(lib, [])
        timeouts = time_stats.get(f'{lib}_timeout', 0)
        if times or timeouts:
            avg = sum(times) / len(times) if times else 0
            max_t = max(times) if times else 0
            print(f"{lib:<15} {len(times):<6} {timeouts:<6} {avg:.2f}s{'':<6} {max_t:.2f}s")
        else:
            print(f"{lib:<15} 未安装或失败")
    print("=" * 50)
    print(f"结果保存在: {OUTPUT_DIR.absolute()}")
    print(f"记录文件: {RECORD_FILE.absolute()}")


if __name__ == "__main__":
    multiprocessing.freeze_support()  # Windows支持
    main()