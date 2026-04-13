"""
kg_extract_test.py — 测试 LLM 输出，调试抽取问题

直接调用 LLM 并返回原始输出，不做任何处理。
"""

import json
import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

from kg_prompts import (
    build_discipline_prompt,
    build_extraction_prompt,
)
from kg_extract import (
    parse_md_metadata,
    _truncate_before_section,
    _truncate_after_section,
    _extract_json_from_response,
)

# 加载环境变量
load_dotenv()

# 配置
API_KEY = os.environ.get("OPENAI_API_KEY", "")
BASE_URL = os.environ.get("OPENAI_BASE_URL", "")
MODEL = os.environ.get("LLM_MODEL", "gpt-4o")
MAX_INPUT_CHARS = int(os.environ.get("MAX_INPUT_CHARS", "100000"))


def test_extraction(md_path: str):
    """测试单个文件的 LLM 输出。"""
    md_file = Path(md_path)
    if not md_file.exists():
        print(f"文件不存在: {md_path}")
        return

    print(f"\n{'='*60}")
    print(f"测试文件: {md_file.name}")
    print(f"{'='*60}\n")

    # 初始化客户端
    client = OpenAI(api_key=API_KEY, base_url=BASE_URL or None)

    # 读取文件
    text = md_file.read_text(encoding="utf-8")
    print(f"原始文本长度: {len(text)} 字符\n")

    # 预处理文本
    paper_text, _ = _truncate_before_section(text, "References", "Bibliography", "参考文献")
    if len(paper_text) > MAX_INPUT_CHARS:
        paper_text, _ = _truncate_after_section(paper_text, "Conclusion", "Conclusions", "结论", "Summary", "总结")
    if len(paper_text) > MAX_INPUT_CHARS:
        paper_text = paper_text[:MAX_INPUT_CHARS]
    print(f"处理后文本长度: {len(paper_text)} 字符\n")

    # 解析元数据
    md_meta = parse_md_metadata(md_file)
    print(f"解析的元数据:")
    print(f"  title: {md_meta.get('title')}")
    print(f"  year: {md_meta.get('year')}")
    print(f"  doi: {md_meta.get('doi')}")
    print()

    # ========== 第一次调用：学科分类 ==========
    print("-" * 40)
    print("第一次 LLM 调用：学科分类")
    print("-" * 40)

    abstract = md_meta.get("abstract") or ""
    introduction = md_meta.get("introduction") or ""

    discipline_sys, discipline_user = build_discipline_prompt(abstract, introduction)

    print(f"\n[System Prompt 长度]: {len(discipline_sys)} 字符")
    print(f"[User Prompt 长度]: {len(discipline_user)} 字符")

    print("\n调用 LLM...")
    discipline_response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": discipline_sys},
            {"role": "user", "content": discipline_user},
        ],
        temperature=0.0,
        response_format={"type": "json_object"}
    )

    discipline_raw = discipline_response.choices[0].message.content or ""
    print(f"\n[原始响应长度]: {len(discipline_raw)} 字符")
    print("\n[原始响应内容]:")
    print(discipline_raw)

    # 尝试解析 JSON
    print("\n[解析后的 JSON]:")
    try:
        discipline_json = _extract_json_from_response(discipline_raw)
        discipline_parsed = json.loads(discipline_json)
        print(json.dumps(discipline_parsed, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"解析失败: {e}")

    # ========== 第二次调用：知识抽取 ==========
    print("\n" + "=" * 60)
    print("第二次 LLM 调用：知识抽取")
    print("=" * 60)

    extraction_sys, extraction_user = build_extraction_prompt(paper_text)

    print(f"\n[System Prompt 长度]: {len(extraction_sys)} 字符")
    print(f"[User Prompt 长度]: {len(extraction_user)} 字符")

    print("\n调用 LLM...")
    extraction_response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": extraction_sys},
            {"role": "user", "content": extraction_user},
        ],
        temperature=0.0,
        response_format={"type": "json_object"}
    )

    extraction_raw = extraction_response.choices[0].message.content or ""
    print(f"\n[原始响应长度]: {len(extraction_raw)} 字符")

    # 保存原始响应到文件
    output_dir = Path("kg_output") / "debug"
    output_dir.mkdir(parents=True, exist_ok=True)

    raw_output_file = output_dir / f"{md_file.stem}_test_raw.json"
    raw_output_file.write_text(extraction_raw, encoding="utf-8")
    print(f"\n[原始响应已保存到]: {raw_output_file}")

    # 尝试解析 JSON
    print("\n[解析后的 JSON]:")
    try:
        extraction_json = _extract_json_from_response(extraction_raw)
        extraction_parsed = json.loads(extraction_json)

        # 检查是否有 entries 字段
        if "entries" in extraction_parsed:
            print(f"✓ 检测到 'entries' 字段，共 {len(extraction_parsed['entries'])} 条记录")

            # 统计各类型数量
            type_counts = {}
            for entry in extraction_parsed["entries"]:
                t = entry.get("type", "unknown")
                type_counts[t] = type_counts.get(t, 0) + 1

            print(f"  类型统计: {type_counts}")
        else:
            print("✗ 未检测到 'entries' 字段")
            print(f"  实际字段: {list(extraction_parsed.keys())}")

        # 打印部分内容
        print("\n[前 3 条记录]:")
        for i, entry in enumerate(extraction_parsed.get("entries", [])[:3]):
            print(f"\n--- Entry {i+1} ---")
            print(json.dumps(entry, ensure_ascii=False, indent=2))

        # 保存解析后的 JSON
        parsed_output_file = output_dir / f"{md_file.stem}_test_parsed.json"
        parsed_output_file.write_text(json.dumps(extraction_parsed, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\n[解析后 JSON 已保存到]: {parsed_output_file}")

    except Exception as e:
        print(f"解析失败: {e}")
        print(f"\n[原始响应前 1000 字符]:\n{extraction_raw[:1000]}")

    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("用法: python kg_extract_test.py <markdown_file>")
        print("示例: python kg_extract_test.py markdown/physics_test.md")
        sys.exit(1)

    test_extraction(sys.argv[1])