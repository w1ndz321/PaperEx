"""
extract.py — 从 markdown/ 中的 MD 文件抽取结构化知识，输出到 output/

用法:
    python extract.py                     # 抽取 markdown/ 下所有 MD
    python extract.py paper.md            # 抽取指定文件
    python extract.py --force             # 强制重新抽取
"""

import json
import re
import sys
import logging
from datetime import datetime, timezone
from pathlib import Path
import os
import yaml
from openai import OpenAI

from prompts import build_prompt, build_metadata_prompt

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent
MARKDOWN_DIR = BASE_DIR / "markdown"
OUTPUT_DIR = BASE_DIR / "output"
CONFIG_PATH = BASE_DIR / "config.yaml"

VALID_TYPES = {"claim", "concept", "method", "dataset", "evaluation_strategy", "metric", "result", "assumption"}

def load_config() -> dict:
    """加载 config.yaml，环境变量优先。"""
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    llm = cfg.get("llm", {})
    llm["api_key"] = os.environ.get("OPENAI_API_KEY", llm.get("api_key", ""))
    llm["base_url"] = os.environ.get("OPENAI_BASE_URL", llm.get("base_url", ""))
    cfg["llm"] = llm
    return cfg


# ─── Markdown 元数据解析 ─────────────────────────────────────

def _strip_md_bold(text: str) -> str:
    """去除 markdown 加粗符号 **...**。"""
    return re.sub(r"\*\*(.*?)\*\*", r"\1", text).strip()


def _extract_section(text: str, heading: str) -> str | None:
    """提取指定标题下到下一个 ## 之间的文本，返回清理后的字符串或 None。"""
    pattern = rf"##\s+\*?\*?{re.escape(heading)}\*?\*?\s*\n(.*?)(?=\n##|\Z)"
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    if not match:
        return None
    return match.group(1).strip()


def parse_md_metadata(md_path: Path) -> dict:
    """从 MD 文件中正则解析 title、year、doi、abstract、keywords。"""
    text = md_path.read_text(encoding="utf-8")

    # title：第一个 # **...** 一级标题
    title = None
    m = re.search(r"^#\s+\*\*(.*?)\*\*", text, re.MULTILINE)
    if m:
        title = m.group(1).strip()

    # doi：优先提取 doi.org/ 后的路径
    doi = None
    m = re.search(r"doi\.org/(10\.\d{4,}/\S+)", text, re.IGNORECASE)
    if m:
        doi = m.group(1).rstrip(".")

    # year：从 "Published: ... YYYY" 或 ACM Reference Format 行中提取
    year = None
    m = re.search(r"Published:.*?(\d{4})", text)
    if not m:
        # 备选：doi 行附近的四位年份
        m = re.search(r"\b(20\d{2})\b", text)
    if m:
        year = int(m.group(1))

    # abstract
    abstract = _extract_section(text, "Abstract")
    # keywords：提取后按分号或逗号分割
    keywords = None
    kw_raw = _extract_section(text, "Keywords")
    if kw_raw:
        kw_raw = _strip_md_bold(kw_raw)
        keywords = [k.strip() for k in re.split(r"[;,]", kw_raw) if k.strip()]

    return {
        "title": title,
        "year": year,
        "doi": doi,
        "abstract": abstract,
        "_keywords_from_paper": keywords,  # 内部字段，后续合并时使用
    }




def validate_entry(raw: dict) -> dict | None:
    """验证单条知识条目，返回规范化的条目或 None（无效时丢弃）。"""
    entry_type = raw.get("type", "")
    if entry_type not in VALID_TYPES:
        logger.debug(f"丢弃无效类型: {entry_type}")
        return None

    text = raw.get("text", "").strip()
    normal_text = raw.get("normal_text", "").strip()
    if not text or not normal_text:
        logger.debug(f"丢弃空条目: text={text!r}")
        return None

    return {
        "type": entry_type,
        "text": text,
        "normal_text": normal_text,
        "topic_tags": raw.get("topic_tags", []),
        "confidence": max(0.0, min(1.0, float(raw.get("confidence", 1.0)))),
        "source_evidence": raw.get("source_evidence"),
    }


# ─── LLM 调用 ────────────────────────────────────────────────

def call_llm(client: OpenAI, model: str, system_prompt: str, user_prompt: str) -> dict:
    """调用 LLM，返回解析后的 dict。失败时重试最多3次。"""
    for attempt in range(3):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.0,
                response_format={"type": "json_object"})
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            logger.warning(f"LLM 调用失败 (第{attempt+1}次): {e}")
            if attempt == 2:
                raise
    return {}
# def call_llm(client: OpenAI, model: str, system_prompt: str, user_prompt: str) -> dict:
#     """调用 LLM，流式输出并返回解析后的 dict。失败时重试最多3次。"""
#     for attempt in range(3):
#         try:
#             chunks = []
#             with client.chat.completions.create(
#                 model=model,
#                 messages=[
#                     {"role": "system", "content": system_prompt},
#                     {"role": "user", "content": user_prompt},
#                 ],
#                 temperature=0.0,
#                 response_format={"type": "json_object"},
#                 stream=True,) as stream:
#                 for chunk in stream:
#                     delta = chunk.choices[0].delta.content
#                     if delta:
#                         print(delta, end="", flush=True)
#                         chunks.append(delta)
#             print()  # 换行
#             return json.loads("".join(chunks))
#         except Exception as e:
#             logger.warning(f"LLM 调用失败 (第{attempt+1}次): {e}")
#             if attempt == 2:
#                 raise
#     return {}

def _remove_section(text: str, *headings: str) -> tuple[str, str | None]:
    """移除正文中指定标题的章节，返回 (处理后文本, 匹配到的标题)。"""
    pattern = r"\n#{1,2}\s+\*?\*?(" + "|".join(re.escape(h) for h in headings) + r")\*?\*?\s*\n"
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return text[:match.start()], match.group(1)
    return text, None




def extract_one(
    md_path: Path, client: OpenAI, model: str,
    max_entries: int = 50, max_input_chars: int = 100000,):
    """对一个 MD 文件执行知识抽取，返回结果字典。"""
    paper_text = md_path.read_text(encoding="utf-8")
    print(f"  文本长度: {len(paper_text)} 字符")

    # 始终移除参考文献
    paper_text, _ = _remove_section(paper_text, "References", "Bibliography", "参考文献")

    # 超出限制时移除附录
    if len(paper_text) > max_input_chars:
        paper_text, removed = _remove_section(paper_text, "Appendix", "Appendices", "附录")
        if removed:
            print(f"  已移除附录（{removed}）")

    # 仍超出限制则硬截断
    if len(paper_text) > max_input_chars:
        print(f"警告: 文本超出上限 {max_input_chars} 字符，已截断（丢弃 {len(paper_text) - max_input_chars} 字符）")
        paper_text = paper_text[:max_input_chars]

    print(f"  处理后文本长度: {len(paper_text)} 字符")

    # ── 解析静态 metadata ──
    md_meta = parse_md_metadata(md_path)
    keywords_from_paper = md_meta.pop("_keywords_from_paper")

    # ── LLM 调用1：从摘要推断学科与关键词 ──
    abstract = md_meta.get("abstract") or ""
    print(f"  调用 LLM 推断 metadata ({model})...")
    meta_sys, meta_user = build_metadata_prompt(abstract)
    meta_parsed = call_llm(client, model, meta_sys, meta_user)

    # keywords：优先使用文中原文
    keywords = keywords_from_paper if keywords_from_paper else meta_parsed.get("keywords", [])

    metadata = {
        "source_file": str(md_path.relative_to(BASE_DIR)),
        "title": md_meta["title"],
        "year": md_meta["year"],
        "doi": md_meta["doi"],
        "abstract": abstract,
        "primary_discipline": meta_parsed.get("primary_discipline"),
        "secondary_disciplines": meta_parsed.get("secondary_disciplines", []),
        "keywords": keywords,
    }

    # ── LLM 调用2：知识条目抽取 ──
    system_prompt, user_prompt = build_prompt(paper_text)
    print(f"  调用 LLM 抽取知识条目 ({model})...")
    parsed = call_llm(client, model, system_prompt, user_prompt)
    raw_entries = parsed.get("entries", [])
    print(f"  LLM 返回 {len(raw_entries)} 条原始条目")

    # 逐条验证，并追加 provenance
    extraction_timestamp = datetime.now(timezone.utc).isoformat()
    entries = []
    for raw in raw_entries:
        entry = validate_entry(raw)
        if entry:
            entry["provenance"] = {
                "model": model,
                "timestamp": extraction_timestamp,
            }
            entries.append(entry)

    # 截断
    notes = None
    if len(entries) > max_entries:
        notes = f"截断: {len(entries)} → {max_entries}"
        entries = entries[:max_entries]

    discarded = len(raw_entries) - len(entries)
    if discarded > 0:
        note = f"丢弃 {discarded} 条无效条目"
        notes = f"{notes}; {note}" if notes else note

    print(f"  有效条目: {len(entries)}")

    return {
        "metadata": metadata,
        "extraction_info": {
            "extraction_model": model,
            "extraction_timestamp": datetime.now(timezone.utc).isoformat(),
            "extraction_notes": notes,
        },
        "entries": entries,
    }



# ─── 主流程 ──────────────────────────────────────────────────

def main():
    logging.basicConfig(level=logging.INFO)
    OUTPUT_DIR.mkdir(exist_ok=True)

    cfg = load_config()
    llm_cfg = cfg["llm"]

    client = OpenAI(
        api_key=llm_cfg["api_key"],
        base_url=llm_cfg["base_url"] or None,
    )
    model = llm_cfg["model"]
    extraction_cfg = cfg.get("extraction", {})
    max_entries = extraction_cfg.get("max_entries_per_paper", 50)
    max_input_chars = extraction_cfg.get("max_input_chars", 100000)
    skip_existing = extraction_cfg.get("skip_existing", True)

    force = "--force" in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("--")]

    # 确定要处理的 MD 文件
    if args:
        md_files = []
        for name in args:
            p = Path(name)
            if not p.is_absolute():
                p = MARKDOWN_DIR / name
            if p.exists():
                md_files.append(p)
            else:
                print(f"文件不存在: {p}")
    else:
        md_files = sorted(MARKDOWN_DIR.glob("*.md"))

    if not md_files:
        print("没有找到 MD 文件")
        return

    print(f"待处理: {len(md_files)} 个文件\n")

    results = {}
    for md_path in md_files:
        out_path = OUTPUT_DIR / f"{md_path.stem}.json"

        if out_path.exists() and skip_existing and not force:
            print(f"[跳过] {md_path.name}（已存在）")
            continue

        print(f"[抽取] {md_path.name}")
        try:
            result = extract_one(md_path, client, model, max_entries, max_input_chars)
            # 保存单篇结果
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            print(f"  → 保存到 {out_path.name}\n")
            results[md_path.stem] = {
                "entry_count": len(result["entries"]),
                "entry_types": {},
            }
            for e in result["entries"]:
                t = e["type"]
                results[md_path.stem]["entry_types"][t] = (
                    results[md_path.stem]["entry_types"].get(t, 0) + 1
                )
        except Exception as e:
            print(f"  ✗ 抽取失败: {e}\n")
            continue

    # 更新 manifest
    manifest_path = OUTPUT_DIR / "manifest.json"
    manifest = {}
    if manifest_path.exists():
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)

    manifest.setdefault("papers", {})
    manifest["papers"].update(results)
    manifest["updated_at"] = datetime.now(timezone.utc).isoformat()
    manifest["total_entries"] = sum(
        p["entry_count"] for p in manifest["papers"].values()
    )

    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print(f"完成。共 {manifest['total_entries']} 条知识条目。")


if __name__ == "__main__":
    main()
