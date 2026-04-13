"""
kg_extract.py — 按照 schema.md 定义的新 schema 从 markdown 论文中抽取知识

8 种知识类型:
1. concept - 概念
2. relation - 关系
3. dataset_and_benchmark - 数据集与基准
4. method_and_experiment - 方法与实验
5. performance_result - 性能结果
6. experimental_parameter - 实验参数与物理量
7. data_specification - 数据规范与标准
8. conclusion_and_insight - 结论与洞见

用法:
    python kg_extract.py                     # 抽取 markdown/ 下所有 MD
    python kg_extract.py paper.md            # 抽取指定文件
    python kg_extract.py --force             # 强制重新抽取
    python kg_extract.py --debug             # 保存处理后的文本和 LLM 响应到 debug/ 目录
"""

import json
import re
import sys
import logging
import hashlib
from datetime import datetime, timezone
from pathlib import Path
import os
from openai import OpenAI
from dotenv import load_dotenv
from kg_prompts import (
    build_discipline_prompt,
    build_extraction_prompt,
)
from kg_schema import (
    LLMExtractionResponse,
    LLMDisciplineResponse,
)

# 加载 .env 文件
load_dotenv()

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent
MARKDOWN_DIR = BASE_DIR / "markdown"
OUTPUT_DIR = BASE_DIR / "kg_output"
DEBUG_DIR = OUTPUT_DIR / "debug"


def load_config() -> dict:
    """从环境变量加载配置。"""
    return {
        "api_key": os.environ.get("OPENAI_API_KEY", ""),
        "base_url": os.environ.get("OPENAI_BASE_URL", ""),
        "model": os.environ.get("LLM_MODEL", "gpt-4o"),
        "temperature": float(os.environ.get("LLM_TEMPERATURE", "0.0")),
        "max_input_chars": int(os.environ.get("MAX_INPUT_CHARS", "100000")),
        "skip_existing": os.environ.get("SKIP_EXISTING", "true").lower() == "true",
    }


def generate_doc_id(title: str | None) -> str:
    """根据标题生成 doc_id。"""
    if title:
        hash_val = hashlib.md5(title.encode()).hexdigest()[:16]
        return f"doc_{hash_val}"
    return f"doc_{hashlib.md5(str(datetime.now()).encode()).hexdigest()[:16]}"


# ─── Markdown 元数据解析 ─────────────────────────────────────

def _strip_md_bold(text: str) -> str:
    """去除 markdown 加粗符号 **...**。"""
    return re.sub(r"\*\*(.*?)\*\*", r"\1", text).strip()


def _extract_section(text: str, heading: str) -> str | None:
    """提取指定标题下到下一个 ## 之间的文本。"""
    pattern = rf"##\s+\*?\*?{re.escape(heading)}\*?\*?\s*\n(.*?)(?=\n##|\Z)"
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    if not match:
        return None
    return match.group(1).strip()


def parse_md_metadata(md_path: Path) -> dict:
    """从 MD 文件中解析 title、year、doi、abstract、introduction。"""
    text = md_path.read_text(encoding="utf-8")

    # title：尝试多种方式提取
    title = None

    # 方法1：匹配一级标题 #，跳过出版信息行
    for line in text.split("\n"):
        if line.startswith("# ") and not line.startswith("# #"):
            candidate = re.sub(r"\*\*(.*?)\*\*", r"\1", line[2:]).strip()
            candidate = re.sub(r"`(.*?)`", r"\1", candidate).strip()
            # 跳过出版信息行
            skip_patterns = [
                "Published in",
                "arXiv:",
                "doi.org",
                "DOI:",
                "FERMILAB",
                "preprint",
                "Draft",
                "Technical Report",
            ]
            if any(p.lower() in candidate.lower() for p in skip_patterns):
                continue
            if len(candidate) < 10:
                continue
            title = candidate
            break

    # 方法2：如果没有一级标题，尝试二级标题 ##
    if not title:
        for line in text.split("\n"):
            if line.startswith("## ") and not line.startswith("## #"):
                candidate = re.sub(r"\*\*(.*?)\*\*", r"\1", line[3:]).strip()
                candidate = re.sub(r"`(.*?)`", r"\1", candidate).strip()
                if len(candidate) < 10:
                    continue
                # 跳过章节名如 Abstract, Introduction 等
                section_names = ["Abstract", "Introduction", "Methods", "Results", "Conclusion", "References"]
                if any(s.lower() in candidate.lower() for s in section_names):
                    continue
                title = candidate
                break

    # 方法3：使用文件名作为 fallback
    if not title:
        title = md_path.stem.replace("_", " ").replace("-", " ")

    # doi
    doi = None
    m = re.search(r"doi\.org/(10\.\d{4,}/\S+)", text, re.IGNORECASE)
    if m:
        doi = m.group(1).rstrip(".")

    # year：从 Published/Date/Received 等关键词后提取
    year = None
    year_patterns = [
        r"\*?\*?Published:?\*?\*?\s*.*?(\d{4})",
        r"\*?\*?Date:?\*?\*?\s*.*?(\d{4})",
        r"Received:?\s*.*?(\d{4})",
        r"Accepted:?\s*.*?(\d{4})",
    ]
    for pattern in year_patterns:
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            year = int(m.group(1))
            break
    if not year:
        m = re.search(r"\b(20[0-2]\d)\b", text)
        if m:
            year = int(m.group(1))

    # abstract
    abstract = _extract_section(text, "Abstract")
    if not abstract:
        lines = text.split("\n")
        for line in lines:
            line_stripped = line.strip()
            if len(line_stripped) > 200 and not line_stripped.startswith("#"):
                abstract = line_stripped
                break

    # introduction
    introduction = None
    for heading in ["Introduction", "INTRODUCTION", "1 Introduction", "1. Introduction", "1\tIntroduction"]:
        introduction = _extract_section(text, heading)
        if introduction:
            break

    # keywords
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
        "introduction": introduction,
        "_keywords_from_paper": keywords,
    }


def _truncate_before_section(text: str, *headings: str) -> tuple[str, str | None]:
    """从指定章节开始截断，丢弃该章节及其之后的所有内容。

    返回 (截断后的文本, 匹配到的章节名)。
    """
    pattern = r"\n#{1,2}\s+\*?\*?(" + "|".join(re.escape(h) for h in headings) + r")\*?\*?\s*"
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return text[:match.start()], match.group(1).strip("*")
    return text, None


def _truncate_after_section(text: str, *headings: str) -> tuple[str, str | None]:
    """保留指定章节，截断其之后的所有内容。

    返回 (截断后的文本, 匹配到的章节名)。
    """
    for heading in headings:
        # 匹配章节标题
        pattern = rf"\n#{1,2}\s+\*?\*?{re.escape(heading)}\*?\*?\s*\n"
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            # 找到下一个同级或更高级标题
            section_start = match.start()
            next_heading = re.search(r"\n#{1,2}\s+", text[match.end():], re.IGNORECASE)
            if next_heading:
                # 截断到下一个标题之前
                truncate_pos = match.end() + next_heading.start()
            else:
                # 没有下一个标题，保留全部
                truncate_pos = len(text)
            return text[:truncate_pos], heading
    return text, None


# ─── LLM 调用 ────────────────────────────────────────────────

def _extract_json_from_response(raw_content: str) -> str:
    """从 LLM 响应中提取 JSON 内容。

    处理情况：
    1. 纯 JSON
    2. 包含 markdown 代码块: ```json ... ```
    3. 包含思考过程: Thinking Process: ... { ... }
    """
    content = raw_content.strip()

    # 方法1：尝试找 markdown 代码块中的 JSON
    if "```json" in content:
        start = content.find("```json") + 7
        end = content.find("```", start)
        if end > start:
            return content[start:end].strip()
    elif "```" in content:
        start = content.find("```") + 3
        end = content.find("```", start)
        if end > start:
            return content[start:end].strip()

    # 方法2：找到第一个 { 或 [ 并提取到对应的结束括号
    for start_char, end_char in [("{", "}"), ("[", "]")]:
        start_idx = content.find(start_char)
        if start_idx >= 0:
            # 找到匹配的结束括号
            depth = 0
            in_string = False
            escape = False
            for i in range(start_idx, len(content)):
                char = content[i]

                if escape:
                    escape = False
                    continue
                if char == "\\":
                    escape = True
                    continue
                if char == '"' and not escape:
                    in_string = not in_string
                    continue

                if not in_string:
                    if char == start_char:
                        depth += 1
                    elif char == end_char:
                        depth -= 1
                        if depth == 0:
                            return content[start_idx:i+1]

    # 方法3：直接返回原内容
    return content


def call_llm(
    client: OpenAI,
    model: str,
    system_prompt: str,
    user_prompt: str,
    temperature: float = 0.0
) -> tuple[dict, str]:
    """调用 LLM，返回 (解析后的 dict, 原始响应文本)。失败时重试最多3次。"""
    last_error = None
    raw_content = ""

    for attempt in range(3):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=temperature,
                response_format={"type": "json_object"})
            raw_content = response.choices[0].message.content or ""

            # 检查是否为空
            if not raw_content.strip():
                raise ValueError("LLM 返回空内容")

            # 提取并解析 JSON
            json_content = _extract_json_from_response(raw_content)
            parsed = json.loads(json_content)
            return parsed, raw_content

        except json.JSONDecodeError as e:
            last_error = e
            logger.warning(f"LLM 调用失败 (第{attempt+1}次): JSON 解析错误 - {e}")
            logger.warning(f"原始响应前500字符: {raw_content[:500]}")
            if attempt == 2:
                raise ValueError(f"LLM 返回的内容无法解析为 JSON: {last_error}")
        except Exception as e:
            last_error = e
            logger.warning(f"LLM 调用失败 (第{attempt+1}次): {e}")
            if attempt == 2:
                raise

    return {}, ""


def validate_discipline_response(raw_response: dict) -> dict:
    """验证学科分类响应。"""
    try:
        validated = LLMDisciplineResponse(**raw_response)
        return validated.model_dump()
    except Exception as e:
        logger.warning(f"学科分类响应验证失败: {e}")
        return raw_response


def validate_extraction_response(raw_response: dict) -> dict:
    """验证抽取响应。"""
    try:
        validated = LLMExtractionResponse(**raw_response)
        return validated.model_dump()
    except Exception as e:
        logger.warning(f"抽取响应验证失败: {e}")
        return raw_response


# ─── 结果组装 ────────────────────────────────────────────────

def _normalize_evidence(item: dict) -> dict:
    """将 LLM 输出的 evidence 格式统一化。

    LLM 可能输出两种格式：
    1. {"evidence": {"section": "...", "original_text": "..."}}
    2. {"original_text": "..."}  (无 evidence 字段)

    返回统一的 evidence dict。
    """
    evidence = item.get("evidence", {})
    if evidence:
        # 已经是正确格式
        return evidence
    # 兼容 original_text 直接字段
    original_text = item.get("original_text", "")
    if original_text:
        return {"section": "", "original_text": original_text}
    return {}


def build_output(
    md_meta: dict,
    discipline_parsed: dict,
    kg_parsed: dict,
    doc_id: str,
    model: str,
) -> dict:
    """将各部分组装成符合 schema 的输出。

    支持两种 LLM 输出格式：
    1. 新格式：{"entries": [...]}  每条记录带 type 字段
    2. 旧格式：{"concepts": [...], "relations": [...], ...}  按类型分组
    """
    extraction_timestamp = datetime.now(timezone.utc).isoformat()

    # metadata 部分
    keywords = md_meta.get("_keywords_from_paper") or discipline_parsed.get("keywords", [])

    metadata = {
        "title": md_meta.get("title"),
        "year": md_meta.get("year"),
        "doi": md_meta.get("doi"),
        "doc_id": doc_id,
        "abstract": md_meta.get("abstract") or "",
        "introduction": md_meta.get("introduction") or "",
        "primary_discipline": discipline_parsed.get("primary_discipline", {"level1": None, "level2": None, "level3": None}),
        "secondary_disciplines": discipline_parsed.get("secondary_disciplines", []),
        "keywords": keywords,
        "extraction_info": {
            "extraction_model": model,
            "extraction_timestamp": extraction_timestamp,
        },
    }

    # 检查是否为新格式（entries 数组）
    if "entries" in kg_parsed:
        entries = _process_entries_format(kg_parsed["entries"], doc_id)
    else:
        # 旧格式：按类型分组
        entries = _process_grouped_format(kg_parsed, doc_id)

    return {
        "metadata": metadata,
        "entries": entries,
    }


def _process_entries_format(entries_raw: list, doc_id: str) -> list:
    """处理新格式：entries 数组，每条记录带 type 字段。"""
    entries = []
    counters = {}

    # concept term -> concept_id 映射（用于 relation）
    concept_terms = {}

    # 第一遍：处理 concept，建立映射
    for item in entries_raw:
        if item.get("type") == "concept":
            term = item.get("term", "").strip()
            if not term:
                continue
            counters["concept"] = counters.get("concept", 0) + 1
            concept_id = f"{doc_id}_c{counters['concept']}"
            concept_terms[term] = concept_id

            entries.append({
                "type": "concept",
                "concept_id": concept_id,
                "term": term,
                "normalized": item.get("normalized", "").strip().lower(),
                "std_label": item.get("std_label", "").strip() or None,
                "evidence": _normalize_evidence(item),
                "confidence": max(0.0, min(1.0, float(item.get("confidence", 1.0)))),
            })

    # 第二遍：处理其他类型
    for item in entries_raw:
        entry_type = item.get("type")
        if entry_type == "concept":
            continue  # 已处理

        if not entry_type:
            continue

        counters[entry_type] = counters.get(entry_type, 0) + 1

        if entry_type == "relation":
            head_term = item.get("head", "").strip()
            tail_term = item.get("tail", "").strip()
            head_id = concept_terms.get(head_term)
            tail_id = concept_terms.get(tail_term)

            # 模糊匹配
            if not head_id:
                for t, cid in concept_terms.items():
                    if head_term.lower() in t.lower() or t.lower() in head_term.lower():
                        head_id = cid
                        break
            if not tail_id:
                for t, cid in concept_terms.items():
                    if tail_term.lower() in t.lower() or t.lower() in tail_term.lower():
                        tail_id = cid
                        break

            if not head_id or not tail_id:
                continue

            entries.append({
                "type": "relation",
                "relation_id": f"{doc_id}_r{counters['relation']}",
                "head": head_id,
                "head_term": head_term,
                "relation_type": item.get("relation_type", "").strip(),
                "relation_surface": item.get("relation_surface", "").strip(),
                "tail": tail_id,
                "tail_term": tail_term,
                "direction": item.get("direction", "directed"),
                "evidence": _normalize_evidence(item),
                "confidence": max(0.0, min(1.0, float(item.get("confidence", 1.0)))),
            })

        elif entry_type == "dataset_and_benchmark":
            datasets = item.get("datasets", [])
            if not datasets and item.get("name"):
                datasets = [{"name": item.get("name"), "role": item.get("role", "used")}]
            entries.append({
                "type": "dataset_and_benchmark",
                "dataset_id": f"{doc_id}_d{counters['dataset_and_benchmark']}",
                "datasets": datasets,
                "evidence": _normalize_evidence(item),
                "confidence": max(0.0, min(1.0, float(item.get("confidence", 1.0)))),
            })

        elif entry_type == "method_and_experiment":
            entries.append({
                "type": "method_and_experiment",
                "method_id": f"{doc_id}_m{counters['method_and_experiment']}",
                "methods": item.get("methods", []),
                "experiment": item.get("experiment", {}),
                "evidence": _normalize_evidence(item),
                "confidence": max(0.0, min(1.0, float(item.get("confidence", 1.0)))),
            })

        elif entry_type == "performance_result":
            entries.append({
                "type": "performance_result",
                "perf_id": f"{doc_id}_p{counters['performance_result']}",
                "metrics": item.get("metrics", []),
                "evidence": _normalize_evidence(item),
                "confidence": max(0.0, min(1.0, float(item.get("confidence", 1.0)))),
            })

        elif entry_type == "experimental_parameter":
            entries.append({
                "type": "experimental_parameter",
                "param_id": f"{doc_id}_e{counters['experimental_parameter']}",
                "parameters": item.get("parameters", []),
                "evidence": _normalize_evidence(item),
                "confidence": max(0.0, min(1.0, float(item.get("confidence", 1.0)))),
            })

        elif entry_type == "data_specification":
            entries.append({
                "type": "data_specification",
                "spec_id": f"{doc_id}_s{counters['data_specification']}",
                "spec_type": item.get("spec_type", ""),
                "related_formats": item.get("related_formats", []),
                "related_domain": item.get("related_domain"),
                "evidence": _normalize_evidence(item),
                "confidence": max(0.0, min(1.0, float(item.get("confidence", 1.0)))),
            })

        elif entry_type == "conclusion_and_insight":
            entries.append({
                "type": "conclusion_and_insight",
                "insight_id": f"{doc_id}_i{counters['conclusion_and_insight']}",
                "insight_type": item.get("insight_type", ""),
                "evidence": _normalize_evidence(item),
                "confidence": max(0.0, min(1.0, float(item.get("confidence", 1.0)))),
            })

    return entries


def _process_grouped_format(kg_parsed: dict, doc_id: str) -> list:
    """处理旧格式：按类型分组（concepts, relations, ...）。"""
    # 键名映射
    key_mapping = {
        "concept": "concepts",
        "relation": "relations",
        "dataset_and_benchmark": "datasets",
        "method_and_experiment": "methods",
        "performance_result": "performances",
        "experimental_parameter": "parameters",
        "data_specification": "specifications",
        "conclusion_and_insight": "insights",
    }
    normalized_kg = {}
    for key, value in kg_parsed.items():
        mapped_key = key_mapping.get(key, key)
        normalized_kg[mapped_key] = value
    kg_parsed = normalized_kg

    entries = []
    counters = {
        "concept": 0,
        "relation": 0,
        "dataset_and_benchmark": 0,
        "method_and_experiment": 0,
        "performance_result": 0,
        "experimental_parameter": 0,
        "data_specification": 0,
        "conclusion_and_insight": 0,
    }

    # concept term -> concept_id 映射
    concept_terms = {}

    # 处理 concepts
    for c in kg_parsed.get("concepts", []):
        term = c.get("term", "").strip()
        if not term:
            continue

        counters["concept"] += 1
        concept_id = f"{doc_id}_c{counters['concept']}"
        concept_terms[term] = concept_id

        entry = {
            "type": "concept",
            "concept_id": concept_id,
            "term": term,
            "normalized": c.get("normalized", "").strip().lower(),
            "std_label": c.get("std_label", "").strip() or None,
            "evidence": _normalize_evidence(c),
            "confidence": max(0.0, min(1.0, float(c.get("confidence", 1.0)))),
        }
        entries.append(entry)

    # 处理 relations
    for r in kg_parsed.get("relations", []):
        head_term = r.get("head", "").strip()
        tail_term = r.get("tail", "").strip()

        # 查找对应的 concept_id
        head_id = concept_terms.get(head_term)
        tail_id = concept_terms.get(tail_term)

        # 模糊匹配
        if not head_id:
            for t, cid in concept_terms.items():
                if head_term.lower() in t.lower() or t.lower() in head_term.lower():
                    head_id = cid
                    break
        if not tail_id:
            for t, cid in concept_terms.items():
                if tail_term.lower() in t.lower() or t.lower() in tail_term.lower():
                    tail_id = cid
                    break

        if not head_id or not tail_id:
            continue

        counters["relation"] += 1
        entry = {
            "type": "relation",
            "relation_id": f"{doc_id}_r{counters['relation']}",
            "head": head_id,
            "head_term": head_term,
            "relation_type": r.get("relation_type", "").strip(),
            "relation_surface": r.get("relation_surface", "").strip(),
            "tail": tail_id,
            "tail_term": tail_term,
            "direction": r.get("direction", "directed"),
            "evidence": _normalize_evidence(r),
            "confidence": max(0.0, min(1.0, float(r.get("confidence", 1.0)))),
        }
        entries.append(entry)

    # 处理 dataset_and_benchmark
    for d in kg_parsed.get("datasets", []):
        nested_datasets = d.get("datasets", [])
        if nested_datasets:
            datasets_list = nested_datasets
        else:
            datasets_list = [d]

        counters["dataset_and_benchmark"] += 1
        entry = {
            "type": "dataset_and_benchmark",
            "dataset_id": f"{doc_id}_d{counters['dataset_and_benchmark']}",
            "datasets": datasets_list,
            "evidence": _normalize_evidence(d),
            "confidence": max(0.0, min(1.0, float(d.get("confidence", 1.0)))),
        }
        entries.append(entry)

    # 处理 method_and_experiment
    for m in kg_parsed.get("methods", []):
        counters["method_and_experiment"] += 1
        entry = {
            "type": "method_and_experiment",
            "method_id": f"{doc_id}_m{counters['method_and_experiment']}",
            "methods": m.get("methods", []),
            "experiment": m.get("experiment", {}),
            "evidence": _normalize_evidence(m),
            "confidence": max(0.0, min(1.0, float(m.get("confidence", 1.0)))),
        }
        entries.append(entry)

    # 处理 performance_result
    for p in kg_parsed.get("performances", []):
        counters["performance_result"] += 1
        entry = {
            "type": "performance_result",
            "perf_id": f"{doc_id}_p{counters['performance_result']}",
            "metrics": p.get("metrics", []),
            "evidence": _normalize_evidence(p),
            "confidence": max(0.0, min(1.0, float(p.get("confidence", 1.0)))),
        }
        entries.append(entry)

    # 处理 experimental_parameter
    for e in kg_parsed.get("parameters", []):
        counters["experimental_parameter"] += 1
        entry = {
            "type": "experimental_parameter",
            "param_id": f"{doc_id}_e{counters['experimental_parameter']}",
            "parameters": e.get("parameters", []),
            "evidence": _normalize_evidence(e),
            "confidence": max(0.0, min(1.0, float(e.get("confidence", 1.0)))),
        }
        entries.append(entry)

    # 处理 data_specification
    for s in kg_parsed.get("specifications", []):
        counters["data_specification"] += 1
        entry = {
            "type": "data_specification",
            "spec_id": f"{doc_id}_s{counters['data_specification']}",
            "spec_type": s.get("spec_type", ""),
            "related_formats": s.get("related_formats", []),
            "related_domain": s.get("related_domain"),
            "evidence": _normalize_evidence(s),
            "confidence": max(0.0, min(1.0, float(s.get("confidence", 1.0)))),
        }
        entries.append(entry)

    # 处理 conclusion_and_insight
    for i in kg_parsed.get("insights", []):
        counters["conclusion_and_insight"] += 1
        entry = {
            "type": "conclusion_and_insight",
            "insight_id": f"{doc_id}_i{counters['conclusion_and_insight']}",
            "insight_type": i.get("insight_type", ""),
            "evidence": _normalize_evidence(i),
            "confidence": max(0.0, min(1.0, float(i.get("confidence", 1.0)))),
        }
        entries.append(entry)

    return entries


# ─── 单文件抽取 ──────────────────────────────────────────────

def extract_one(
    md_path: Path,
    client: OpenAI,
    model: str,
    max_input_chars: int = 100000,
    temperature: float = 0.0,
    debug: bool = False,
) -> tuple[dict, dict]:
    """对一个 MD 文件执行知识抽取，返回 (结果字典, debug信息)。"""
    original_text = md_path.read_text(encoding="utf-8")
    paper_text = original_text
    original_len = len(paper_text)
    debug_info = {
        "original_length": original_len,
        "operations": [],
        "llm_responses": {},  # 保存 LLM 原始响应
    }

    print(f"  文本长度: {original_len} 字符")

    # 丢弃 References 及之后的所有内容
    paper_text, removed_ref = _truncate_before_section(paper_text, "References", "Bibliography", "参考文献")
    if removed_ref:
        debug_info["operations"].append({"action": "truncate_before", "section": removed_ref})
        print(f"  已丢弃 {removed_ref} 及之后的内容")

    # 如果仍超长，保留 Conclusion，丢弃之后的内容
    if len(paper_text) > max_input_chars:
        paper_text, truncated_section = _truncate_after_section(paper_text, "Conclusion", "Conclusions", "结论", "Summary", "总结")
        if truncated_section:
            debug_info["operations"].append({"action": "truncate_after", "section": truncated_section})
            print(f"  已保留 {truncated_section}，丢弃其之后的内容")

    # 硬截断（最后的保险）
    if len(paper_text) > max_input_chars:
        truncated_len = len(paper_text) - max_input_chars
        paper_text = paper_text[:max_input_chars]
        debug_info["operations"].append({
            "action": "hard_truncate",
            "from_length": len(paper_text) + truncated_len,
            "to_length": max_input_chars,
            "truncated_chars": truncated_len,
        })
        print(f"  警告: 硬截断至 {max_input_chars} 字符（丢弃 {truncated_len} 字符）")

    debug_info["processed_length"] = len(paper_text)
    debug_info["processed_text"] = paper_text
    print(f"  处理后文本长度: {len(paper_text)} 字符")

    # 解析静态 metadata
    md_meta = parse_md_metadata(md_path)
    doc_id = generate_doc_id(md_meta.get("title"))

    # LLM 调用1：推断学科
    abstract = md_meta.get("abstract") or ""
    introduction = md_meta.get("introduction") or ""
    print(f"  调用 LLM 推断学科 ({model})...")
    discipline_sys, discipline_user = build_discipline_prompt(abstract, introduction)
    discipline_parsed, discipline_raw = call_llm(client, model, discipline_sys, discipline_user, temperature)
    discipline_parsed = validate_discipline_response(discipline_parsed)
    debug_info["llm_responses"]["discipline"] = discipline_raw
    if debug:
        print(f"    学科分类原始响应: {discipline_raw[:200]}...")

    # LLM 调用2：抽取知识
    extraction_sys, extraction_user = build_extraction_prompt(paper_text)
    print(f"  调用 LLM 抽取知识 ({model})...")
    kg_parsed, extraction_raw = call_llm(client, model, extraction_sys, extraction_user, temperature)
    kg_parsed = validate_extraction_response(kg_parsed)
    debug_info["llm_responses"]["extraction"] = extraction_raw
    if debug:
        print(f"    抽取响应长度: {len(extraction_raw)} 字符")

    # 组装输出
    result = build_output(md_meta, discipline_parsed, kg_parsed, doc_id, model)

    # 统计
    type_counts = {}
    for e in result["entries"]:
        t = e["type"]
        type_counts[t] = type_counts.get(t, 0) + 1
    print(f"  有效条目: {len(result['entries'])} 条")
    for t, c in type_counts.items():
        print(f"    - {t}: {c}")

    return result, debug_info


# ─── 主流程 ──────────────────────────────────────────────────

def main():
    logging.basicConfig(level=logging.INFO)
    OUTPUT_DIR.mkdir(exist_ok=True)

    cfg = load_config()

    if not cfg["api_key"]:
        print("错误: 未设置 OPENAI_API_KEY")
        return

    client = OpenAI(
        api_key=cfg["api_key"],
        base_url=cfg["base_url"] or None,
    )
    model = cfg["model"]
    max_input_chars = cfg["max_input_chars"]
    temperature = cfg["temperature"]
    skip_existing = cfg["skip_existing"]

    force = "--force" in sys.argv
    debug = "--debug" in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("--")]

    if debug:
        DEBUG_DIR.mkdir(exist_ok=True)
        print("[debug 模式] 处理后的文本和 LLM 响应将保存到 kg_output/debug/ 目录\n")

    # 确定要处理的文件
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

    # 加载已有的统计（累积）
    stats_path = OUTPUT_DIR / "stats.json"
    if stats_path.exists():
        with open(stats_path, "r", encoding="utf-8") as f:
            stats = json.load(f)
        print(f"[累积统计] 已有 {stats.get('total_entries', 0)} 条记录，{len(stats.get('papers', {}))} 篇论文\n")
    else:
        stats = {"total_entries": 0, "type_counts": {}, "papers": {}}

    for md_path in md_files:
        out_path = OUTPUT_DIR / f"{md_path.stem}.json"

        if out_path.exists() and skip_existing and not force:
            # 跳过时，从已有结果读取统计
            existing_result = json.loads(out_path.read_text(encoding="utf-8"))
            entry_count = len(existing_result.get("entries", []))
            stats["papers"][md_path.stem] = {"entries": entry_count, "status": "skipped"}
            print(f"[跳过] {md_path.name}（已存在，{entry_count} 条记录）")
            continue

        print(f"[抽取] {md_path.name}")
        try:
            # 统计 - 先读取旧数据（如果是重新抽取），在保存新结果之前
            old_paper_stats = stats.get("papers", {}).get(md_path.stem, {})
            old_type_counts = {}
            if old_paper_stats and old_paper_stats.get("entries"):
                old_count = old_paper_stats.get("entries", 0)
                # 从已有的 output 文件读取旧的 type_counts（在保存新结果之前）
                if out_path.exists():
                    old_result = json.loads(out_path.read_text(encoding="utf-8"))
                    for e in old_result.get("entries", []):
                        t = e["type"]
                        old_type_counts[t] = old_type_counts.get(t, 0) + 1
                    # 减去旧的统计
                    stats["total_entries"] -= old_count
                    for t, c in old_type_counts.items():
                        if stats["type_counts"].get(t, 0) >= c:
                            stats["type_counts"][t] -= c
                        elif stats["type_counts"].get(t, 0) > 0:
                            stats["type_counts"][t] = 0

            result, debug_info = extract_one(md_path, client, model, max_input_chars, temperature, debug)

            # 保存结果
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            print(f"  → 保存到 {out_path.name}\n")

            # debug 模式下保存处理后的文本和 LLM 响应
            if debug:
                # 保存处理后的文本
                debug_path = DEBUG_DIR / f"{md_path.stem}_processed.md"
                debug_path.write_text(debug_info["processed_text"], encoding="utf-8")

                # 保存 LLM 原始响应
                llm_responses = debug_info.get("llm_responses", {})
                if llm_responses.get("discipline"):
                    discipline_resp_path = DEBUG_DIR / f"{md_path.stem}_llm_discipline.json"
                    discipline_resp_path.write_text(llm_responses["discipline"], encoding="utf-8")
                if llm_responses.get("extraction"):
                    extraction_resp_path = DEBUG_DIR / f"{md_path.stem}_llm_extraction.json"
                    extraction_resp_path.write_text(llm_responses["extraction"], encoding="utf-8")

                # 保存 debug 元信息
                debug_meta_path = DEBUG_DIR / f"{md_path.stem}_debug.json"
                debug_meta = {
                    "original_length": debug_info["original_length"],
                    "processed_length": debug_info["processed_length"],
                    "operations": debug_info["operations"],
                    "llm_response_files": {
                        "discipline": f"{md_path.stem}_llm_discipline.json" if llm_responses.get("discipline") else None,
                        "extraction": f"{md_path.stem}_llm_extraction.json" if llm_responses.get("extraction") else None,
                    }
                }
                debug_meta_path.write_text(json.dumps(debug_meta, ensure_ascii=False, indent=2), encoding="utf-8")
                print(f"  [debug] 保存到 debug/{md_path.stem}_*\n")

            # 添加新的统计
            entry_count = len(result["entries"])
            stats["total_entries"] += entry_count
            stats["papers"][md_path.stem] = {"entries": entry_count, "status": "extracted"}

            for e in result["entries"]:
                t = e["type"]
                stats["type_counts"][t] = stats["type_counts"].get(t, 0) + 1

        except Exception as e:
            print(f"  ✗ 抽取失败: {e}\n")
            continue

    # 保存统计
    stats["updated_at"] = datetime.now(timezone.utc).isoformat()
    stats_path = OUTPUT_DIR / "stats.json"
    with open(stats_path, "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

    print(f"\n完成。")
    print(f"  总记录: {stats['total_entries']} 条")
    print(f"  论文数: {len(stats.get('papers', {}))} 篇")
    print(f"  类型分布:")
    for t, c in sorted(stats.get("type_counts", {}).items()):
        print(f"    - {t}: {c}")


if __name__ == "__main__":
    main()