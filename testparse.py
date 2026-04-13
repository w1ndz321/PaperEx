"""
PDF解析库性能测试脚本
测试库：pypdf, pymupdf, pymupdf4llm, markitdown, pdfplumber
"""

import os
import time
import json
import multiprocessing
from pathlib import Path
from typing import Optional, Tuple

# 超时限制（秒）
TIMEOUT_LIMIT = 100


class TimeoutException(Exception):
    """超时异常"""
    pass


def run_with_timeout(func, args, timeout):
    """带超时执行函数，返回 (结果, 是否超时, 耗时)"""
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


def find_all_pdfs(papers_dir: str) -> list:
    """递归查找所有PDF文件"""
    pdf_files = []
    papers_path = Path(papers_dir)
    for pdf_path in papers_path.rglob("*.pdf"):
        pdf_files.append(str(pdf_path))
    return sorted(pdf_files)


def parse_with_pypdf(pdf_path: str) -> str:
    """使用pypdf解析PDF"""
    from pypdf import PdfReader
    reader = PdfReader(pdf_path)
    text_content = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            text_content.append(text)
    return "\n\n".join(text_content)


def parse_with_pymupdf(pdf_path: str) -> str:
    """使用pymupdf解析PDF"""
    import fitz  # pymupdf
    doc = fitz.open(pdf_path)
    text_content = []
    for page in doc:
        text = page.get_text()
        if text:
            text_content.append(text)
    doc.close()
    return "\n\n".join(text_content)


def parse_with_pymupdf4llm(pdf_path: str) -> str:
    """使用pymupdf4llm解析PDF，直接输出markdown"""
    import pymupdf4llm
    md_text = pymupdf4llm.to_markdown(pdf_path)
    return md_text


def parse_with_markitdown(pdf_path: str) -> str:
    """使用markitdown解析PDF"""
    from markitdown import MarkItDown
    md = MarkItDown()
    result = md.convert(pdf_path)
    return result.text_content


def parse_with_pdfplumber(pdf_path: str) -> str:
    """使用pdfplumber解析PDF"""
    import pdfplumber
    text_content = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                text_content.append(text)
    return "\n\n".join(text_content)


def text_to_markdown(text: str, pdf_name: str) -> str:
    """将纯文本转换为简单的markdown格式"""
    lines = text.split('\n')
    md_lines = [f"# {pdf_name}\n"]

    for line in lines:
        line = line.strip()
        if line:
            md_lines.append(line)

    return '\n'.join(md_lines)


def process_pdf(pdf_path: str, parser_func, parser_name: str, output_dir: str) -> Tuple[bool, float, Optional[str]]:
    """
    处理单个PDF文件
    返回：(是否成功, 处理时间, 错误信息)
    """
    pdf_name = Path(pdf_path).stem
    relative_path = Path(pdf_path).relative_to("papers")
    output_path = Path(output_dir) / relative_path.parent / f"{pdf_name}.md"

    # 创建输出目录
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # 使用 multiprocessing 超时机制
    result, status, elapsed = run_with_timeout(parser_func, (pdf_path,), TIMEOUT_LIMIT)

    if status is True:  # 超时
        return False, elapsed, "超时"
    elif isinstance(status, str):  # 错误
        return False, elapsed, status
    else:  # 成功
        content = result
        # 如果不是markdown输出，转换成markdown
        if parser_name not in ['pymupdf4llm', 'markitdown']:
            content = text_to_markdown(content, pdf_name)

        # 保存结果（在主进程中）
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return True, elapsed, None


def run_benchmark():
    """运行基准测试"""
    # 解析器配置
    parsers = {
        'pypdf': parse_with_pypdf,
        'pymupdf': parse_with_pymupdf,
        'pymupdf4llm': parse_with_pymupdf4llm,
        'markitdown': parse_with_markitdown,
        'pdfplumber': parse_with_pdfplumber
    }

    # 查找所有PDF文件
    papers_dir = "papers"
    pdf_files = find_all_pdfs(papers_dir)
    print(f"找到 {len(pdf_files)} 个PDF文件")

    # 结果统计
    results = {name: {
        'times': [],
        'errors': [],
        'timeouts': [],
        'file_details': []
    } for name in parsers.keys()}

    # 对每个解析器进行测试
    for parser_name, parser_func in parsers.items():
        print(f"\n{'='*60}")
        print(f"正在测试: {parser_name}")
        print('='*60)

        output_dir = f"parsed_results/{parser_name}"
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        for idx, pdf_path in enumerate(pdf_files, 1):
            pdf_name = Path(pdf_path).name
            print(f"[{idx}/{len(pdf_files)}] 处理: {pdf_name}...", end=" ")

            success, elapsed_time, error = process_pdf(
                pdf_path, parser_func, parser_name, output_dir
            )

            if success:
                print(f"✓ ({elapsed_time:.2f}秒)")
                results[parser_name]['times'].append(elapsed_time)
                results[parser_name]['file_details'].append({
                    'file': pdf_path,
                    'time': elapsed_time,
                    'status': 'success'
                })
            else:
                if 'timeout' in str(error).lower() or elapsed_time >= TIMEOUT_LIMIT:
                    print(f"⏱ 超时 ({elapsed_time:.2f}秒)")
                    results[parser_name]['timeouts'].append(pdf_path)
                    results[parser_name]['file_details'].append({
                        'file': pdf_path,
                        'time': elapsed_time,
                        'status': 'timeout'
                    })
                else:
                    print(f"✗ 错误: {error}")
                    results[parser_name]['errors'].append({
                        'file': pdf_path,
                        'error': str(error)
                    })
                    results[parser_name]['file_details'].append({
                        'file': pdf_path,
                        'time': elapsed_time,
                        'status': 'error',
                        'error': str(error)
                    })

    # 生成统计报告
    print("\n" + "="*60)
    print("性能统计报告")
    print("="*60)

    report = {
        'test_time': time.strftime('%Y-%m-%d %H:%M:%S'),
        'total_files': len(pdf_files),
        'timeout_limit': TIMEOUT_LIMIT,
        'parsers': {}
    }

    for parser_name in parsers.keys():
        times = results[parser_name]['times']

        if times:
            avg_time = sum(times) / len(times)
            max_time = max(times)
            min_time = min(times)
            success_count = len(times)
        else:
            avg_time = max_time = min_time = 0
            success_count = 0

        parser_report = {
            'total_files': len(pdf_files),
            'success_count': success_count,
            'timeout_count': len(results[parser_name]['timeouts']),
            'error_count': len(results[parser_name]['errors']),
            'average_time': round(avg_time, 3),
            'max_time': round(max_time, 3),
            'min_time': round(min_time, 3),
            'file_details': results[parser_name]['file_details'],
            'errors': results[parser_name]['errors']
        }

        report['parsers'][parser_name] = parser_report

        print(f"\n{parser_name}:")
        print(f"  成功: {success_count}/{len(pdf_files)}")
        print(f"  超时: {len(results[parser_name]['timeouts'])}")
        print(f"  错误: {len(results[parser_name]['errors'])}")
        print(f"  平均时间: {avg_time:.3f}秒")
        print(f"  最长时间: {max_time:.3f}秒")
        print(f"  最短时间: {min_time:.3f}秒")

    # 保存详细报告
    report_path = "parsed_results/performance_report.json"
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"\n详细报告已保存到: {report_path}")

    # 同时生成一个可读的markdown报告
    generate_markdown_report(report)


def generate_markdown_report(report: dict):
    """生成Markdown格式的报告"""
    md_lines = [
        "# PDF解析库性能测试报告",
        f"\n**测试时间**: {report['test_time']}",
        f"**测试文件数**: {report['total_files']}",
        f"**超时限制**: {report['timeout_limit']}秒\n",
        "---\n"
    ]

    # 总览表格
    md_lines.append("## 总体性能对比\n")
    md_lines.append("| 解析库 | 成功数 | 超时数 | 错误数 | 平均时间(秒) | 最长时间(秒) | 最短时间(秒) |")
    md_lines.append("|--------|--------|--------|--------|--------------|--------------|--------------|")

    for parser_name, data in report['parsers'].items():
        md_lines.append(
            f"| {parser_name} | {data['success_count']} | {data['timeout_count']} | "
            f"{data['error_count']} | {data['average_time']} | {data['max_time']} | {data['min_time']} |"
        )

    md_lines.append("\n---\n")

    # 详细信息
    md_lines.append("## 各解析库详细结果\n")

    for parser_name, data in report['parsers'].items():
        md_lines.append(f"### {parser_name}\n")
        md_lines.append(f"- 成功: {data['success_count']}/{data['total_files']}")
        md_lines.append(f"- 平均时间: {data['average_time']}秒")
        md_lines.append(f"- 最长时间: {data['max_time']}秒")

        if data['errors']:
            md_lines.append(f"\n**错误文件:**")
            for err in data['errors']:
                md_lines.append(f"- `{Path(err['file']).name}`: {err['error'][:100]}")

        md_lines.append("")

    # 按解析速度排序
    md_lines.append("## 性能排名\n")
    sorted_parsers = sorted(
        report['parsers'].items(),
        key=lambda x: x[1]['average_time'] if x[1]['average_time'] > 0 else float('inf')
    )

    for idx, (parser_name, data) in enumerate(sorted_parsers, 1):
        if data['average_time'] > 0:
            md_lines.append(f"{idx}. **{parser_name}**: 平均 {data['average_time']}秒")

    # 保存报告
    report_md_path = "parsed_results/performance_report.md"
    with open(report_md_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(md_lines))

    print(f"Markdown报告已保存到: {report_md_path}")


if __name__ == "__main__":
    multiprocessing.freeze_support()  # Windows支持
    run_benchmark()