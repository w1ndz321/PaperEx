"""
kg_extract.py — 知识抽取：读 MD + 读 kg_meta → 调 LLM 抽取 10 类知识 → 写 kg_output

输入: markdown/*.md + kg_meta/*.json
输出: kg_output/*.json (metadata 来自 kg_meta，entries 来自 LLM 抽取)

流程:
    1. 读 MD 全文，超过 max_input_chars 则截断
    2. 读 kg_meta/*.json 获取 metadata + 学科分类（preprocess 已完成）
    3. 调 1 次 LLM: 知识抽取（10 类知识条目）
    4. 组装最终 JSON: metadata + entries，写出 kg_output/*.json

10 种知识类型: concept, relation, dataset, method, experiment,
              performance_result, conclusion, claim, future_work, limitation
"""

import json
import re
import sys
import time
import random
import logging
import hashlib
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
import os
from openai import OpenAI, RateLimitError, APIConnectionError, APITimeoutError
from dotenv import load_dotenv
from kg_prompts import build_extraction_prompt
from kg_schema import LLMExtractionResponse

load_dotenv()
logger = logging.getLogger(__name__)
BASE_DIR = Path(__file__).parent
MARKDOWN_DIR = BASE_DIR / "markdown"
OUTPUT_DIR = BASE_DIR / "kg_output"
DEBUG_DIR = OUTPUT_DIR / "debug"

PUB_METADATA_SKIP = [
    "Published in", "arXiv:", "doi.org", "DOI:", "FERMILAB",
    "preprint", "Draft", "Technical Report",
    "Chem Soc Rev", "Chem. Soc. Rev.", "Nature", "Science", "Cell", "PNAS",
    "JACS", "Angew", "Adv. Mater.", "Adv. Sci.", "Phys. Rev.", "IEEE",
    "TUTORIAL REVIEW", "REVIEW", "ARTICLE", "LETTER", "PERSPECTIVE",
]
SECTION_NAMES = ["Abstract", "Introduction", "Methods", "Results", "Conclusion", "References", "Key learning points"]

TYPE_META = {
    "concept":            {"prefix": "c",  "id_field": "concept_id"},
    "relation":           {"prefix": "r",  "id_field": "relation_id"},
    "dataset":            {"prefix": "d",  "id_field": "dataset_id"},
    "method":             {"prefix": "m",  "id_field": "method_id"},
    "experiment":         {"prefix": "x",  "id_field": "experiment_id"},
    "performance_result": {"prefix": "p",  "id_field": "perf_id"},
    "conclusion":         {"prefix": "cl", "id_field": "conclusion_id"},
    "claim":              {"prefix": "ca", "id_field": "claim_id"},
    "future_work":        {"prefix": "fw", "id_field": "future_work_id"},
    "limitation":         {"prefix": "lm", "id_field": "limitation_id"},
}
TYPE_FIELDS = {
    "concept": ["term", "normalized", "std_label"],
    "relation": ["head", "relation_type", "relation_surface", "tail"],
    "dataset": ["name", "samples", "domain"],
    "method": ["name", "method_type"],
    "experiment": ["task"],
}
GROUP_KEYS = {
    "concepts": "concept", "relations": "relation", "datasets": "dataset",
    "methods": "method", "experiments": "experiment", "performances": "performance_result",
    "conclusions": "conclusion", "claims": "claim", "future_works": "future_work",
    "limitations": "limitation",
}


def load_config():
    return {
        "api_key": os.environ.get("OPENAI_API_KEY", ""),
        "base_url": os.environ.get("OPENAI_BASE_URL", ""),
        "model": os.environ.get("LLM_MODEL", "gpt-4o"),
        "temperature": float(os.environ.get("LLM_TEMPERATURE", "0.0")),
        "max_input_chars": int(os.environ.get("MAX_INPUT_CHARS", "100000")),
        "metadata_head_chars": int(os.environ.get("METADATA_HEAD_CHARS", "3000")),
        "max_output_tokens": int(os.environ.get("MAX_OUTPUT_TOKENS", "16384")),
        "skip_existing": os.environ.get("SKIP_EXISTING", "true").lower() == "true",
        "workers": int(os.environ.get("WORKERS", "1")),
        "max_retries": int(os.environ.get("MAX_RETRIES", "5")),
        "min_md_chars": int(os.environ.get("MIN_MD_CHARS", "10000")),
        "process_limit": int(os.environ.get("PROCESS_LIMIT", "0")) or None,
    }


def generate_doc_id(title: str | None, stem: str = "") -> str:
    src = (title or "") + "|" + stem
    return f"doc_{hashlib.md5(src.encode()).hexdigest()[:16]}"


# ─── 正则提取 metadata（供 preprocess 使用）────────────────────

def _strip_md(text: str) -> str:
    return re.sub(r"\*\*(.*?)\*\*", r"\1", text).strip()


def _extract_section(text: str, heading: str) -> str | None:
    m = re.search(rf"##\s+\*?\*?{re.escape(heading)}\*?\*?\s*\n(.*?)(?=\n##|\Z)", text, re.DOTALL | re.IGNORECASE)
    return m.group(1).strip() if m else None


def parse_md_metadata(text: str, md_path: Path) -> dict:
    """正则提取 title/year/doi/abstract/introduction/keywords。结果供 preprocess 兜底使用。"""
    title = None
    for line in text.split("\n"):
        if line.startswith("# ") and not line.startswith("# #"):
            c = _strip_md(re.sub(r"`(.*?)`", r"\1", line[2:]))
            if len(c) < 15 or any(p.lower() in c.lower() for p in PUB_METADATA_SKIP): continue
            for pat in [r"\bCite\s*this[:\s].*?(DOI[:\s]*[0-9./]+)?", r"\bDOI[:\s]*10\.\d{4,}/[^\s]+"]:
                m = re.search(pat, c, re.IGNORECASE)
                if m:
                    b, a = c[:m.start()].strip(), c[m.end():].strip()
                    if b and a and len(b) > 10 and len(a) > 3: c = b + " " + a
                    elif b and len(b) > 15: c = b
                    elif a and len(a) > 15: c = a
            for p in ["view article online", "view journal", "download pdf", "full text"]:
                idx = c.lower().find(p)
                if idx >= 0: c = c[:idx].strip()
            c = re.sub(r"\s+[\*†§#†‡]+\s*$", "", c)
            c = re.sub(r"\s+[0-9]+-[0-9]+\s*$", "", c)
            c = re.sub(r"\s*\([12][0-9]{3}\)\s*$", "", c)
            c = re.sub(r"\s+", " ", c).strip()
            if len(c) >= 10: title = c
            break
    if not title:
        skip = PUB_METADATA_SKIP + ["View Article Online", "View Journal"]
        for line in text.split("\n"):
            if line.startswith("## ") and not line.startswith("## #"):
                c = _strip_md(re.sub(r"`(.*?)`", r"\1", line[3:]))
                if any(s.lower() in c.lower() for s in SECTION_NAMES + skip): continue
                c = re.sub(r"\s+", " ", c).strip()
                if len(c) >= 15: title = c; break
    if not title:
        title = md_path.stem.replace("_", " ").replace("-", " ")

    doi = m.group(1).rstrip(".") if (m := re.search(r"doi\.org/(10\.\d{4,}/\S+)", text, re.IGNORECASE)) else None

    year = None
    for pat in [
        r"(?:Date|Published|Publication\s*date|Submitted|Posted)\s*[:\s]\s*.*?(\d{4})",
        r"\*?\*?(?:Date|Published)\s*:?\s*\*?\*?\s*.*?(\d{4})",
        r"(?:Received|Accepted|Revised)\s*[:\s]\s*.*?(\d{4})",
    ]:
        if (m := re.search(pat, text, re.IGNORECASE)):
            year = int(m.group(1))
            if 1990 <= year <= 2030: break
            year = None
    if not year:
        if (m := re.search(r"©\s*(\d{4})", text)) or (m := re.search(r"\b(20[0-2]\d)\b", text)):
            year = int(m.group(1))

    abstract = _extract_section(text, "Abstract")
    if not abstract:
        for line in text.split("\n"):
            ls = line.strip()
            if len(ls) > 200 and not ls.startswith("#"): abstract = ls; break

    introduction = None
    for h in ["Introduction", "INTRODUCTION", "1 Introduction", "1. Introduction", "1\tIntroduction"]:
        if (introduction := _extract_section(text, h)): break

    keywords = None
    kw_raw = _extract_section(text, "Keywords")
    if kw_raw:
        keywords = [k.strip() for k in re.split(r"[;,]", _strip_md(kw_raw)) if k.strip()]

    return {"title": title, "year": year, "doi": doi, "abstract": abstract, "introduction": introduction, "_keywords_from_paper": keywords}


# ─── LLM 调用 ───────────────────────────────────────────────

def _extract_json(raw: str) -> str:
    for tag in ["```json", "```"]:
        if tag in raw:
            s, e = raw.find(tag) + len(tag), raw.find("```", raw.find(tag) + len(tag))
            if e > s:
                return raw[s:e].strip()
    for sc, ec in [("{", "}"), ("[", "]")]:
        si = raw.find(sc)
        if si >= 0:
            depth, in_str, esc = 0, False, False
            for i in range(si, len(raw)):
                c = raw[i]
                if esc: esc = False; continue
                if c == "\\": esc = True; continue
                if c == '"': in_str = not in_str; continue
                if not in_str:
                    depth += (1 if c == sc else -1 if c == ec else 0)
                    if depth == 0: return raw[si:i+1]
    return raw


def _sanitize(obj):
    if isinstance(obj, dict): return {k: _sanitize(v) for k, v in obj.items()}
    if isinstance(obj, list): return [_sanitize(x) for x in obj]
    if isinstance(obj, int) and not isinstance(obj, bool) and abs(obj) >= 10**1000:
        return str(obj)
    return obj


def call_llm(client, model, sys_prompt, user_prompt, temperature, stream=False, max_tokens=16384, max_retries=5):
    """调 LLM，返回 (parsed_dict, raw_str, usage_dict)。按错误类型指数退避重试。"""
    kwargs = dict(model=model, temperature=temperature, max_tokens=max_tokens,
                  messages=[{"role": "system", "content": sys_prompt},
                            {"role": "user", "content": user_prompt}])
    if not model.startswith("gemini"):
        kwargs["response_format"] = {"type": "json_object"}
    if model.startswith("qwen"):
        kwargs["extra_body"] = {"enable_thinking": False}
    raw, usage = "", {}
    for attempt in range(max_retries):
        try:
            if stream:
                last, raw = None, ""
                for chunk in client.chat.completions.create(stream=True, stream_options={"include_usage": True}, **kwargs):
                    last = chunk
                    if chunk.choices and chunk.choices[0].delta.content:
                        raw += chunk.choices[0].delta.content
                        print(chunk.choices[0].delta.content, end="", flush=True)
                print()
                if last and last.usage:
                    usage = {"prompt_tokens": last.usage.prompt_tokens, "completion_tokens": last.usage.completion_tokens, "total_tokens": last.usage.total_tokens}
            else:
                resp = client.chat.completions.create(**kwargs)
                raw = resp.choices[0].message.content or ""
                if resp.usage:
                    usage = {"prompt_tokens": resp.usage.prompt_tokens, "completion_tokens": resp.usage.completion_tokens, "total_tokens": resp.usage.total_tokens}
            if not raw.strip():
                raise ValueError("LLM 返回空内容")
            extracted = _extract_json(raw)
            start = next((i for i, c in enumerate(extracted) if c in "{["), 0)
            obj, _ = json.JSONDecoder().raw_decode(extracted, start)
            return _sanitize(obj), raw, usage
        except RateLimitError as e:
            # 限流：等待时间更长
            wait = 2 ** attempt + random.uniform(0, 1)
            logger.warning(f"限流 ({attempt+1}/{max_retries})，等待 {wait:.1f}s: {e}")
            if attempt == max_retries - 1: raise
            time.sleep(wait)
        except (APIConnectionError, APITimeoutError) as e:
            # 网络错误：指数退避
            wait = 2 ** attempt
            logger.warning(f"网络错误 ({attempt+1}/{max_retries})，等待 {wait}s: {e}")
            if attempt == max_retries - 1: raise
            time.sleep(wait)
        except json.JSONDecodeError as e:
            # JSON 解析失败：不等待，直接重试
            logger.warning(f"JSON 解析错误 ({attempt+1}/{max_retries}): {e}")
            if attempt == max_retries - 1: raise ValueError(f"LLM 返回无法解析为 JSON: {e}")
        except Exception as e:
            logger.warning(f"LLM 错误 ({attempt+1}/{max_retries}): {e}")
            if attempt == max_retries - 1: raise
    return {}, "", {}


# ─── 知识条目构建 ────────────────────────────────────────────

def _normalize_evidence(item: dict) -> dict:
    ev = item.get("evidence", {})
    if ev: return ev
    ot = item.get("original_text", "")
    return {"section": "", "original_text": ot} if ot else {}


def _make_entry(item: dict, entry_type: str, doc_id: str, counters: dict, concept_terms: dict) -> dict | None:
    meta = TYPE_META[entry_type]
    counters[entry_type] = counters.get(entry_type, 0) + 1
    eid = f"{doc_id}_{meta['prefix']}{counters[entry_type]}"
    entry = {"type": entry_type, meta["id_field"]: eid, "evidence": _normalize_evidence(item),
             "confidence": max(0.0, min(1.0, float(item.get("confidence", 1.0))))}
    for f in TYPE_FIELDS.get(entry_type, []):
        entry[f] = item.get(f)
    if entry_type == "relation":
        head, tail = item.get("head", "").strip(), item.get("tail", "").strip()
        hid = concept_terms.get(head) or next((cid for t, cid in concept_terms.items() if t.lower() == head.lower()), None)
        if not hid:
            hid = next((cid for t, cid in concept_terms.items() if head.lower() in t.lower() or t.lower() in head.lower()), None)
        tid = concept_terms.get(tail) or next((cid for t, cid in concept_terms.items() if t.lower() == tail.lower()), None)
        if not tid:
            tid = next((cid for t, cid in concept_terms.items() if tail.lower() in t.lower() or t.lower() in tail.lower()), None)
        if not hid or not tid: return None
        entry["head"], entry["tail"] = hid, tid
    if entry_type == "dataset" and not item.get("name"):
        return None
    return entry


def build_entries(entries_raw: list, doc_id: str, counters: dict, concept_terms: dict) -> list:
    entries = []
    for item in entries_raw:
        t = item.get("type")
        if not t or t not in TYPE_META: continue
        if t == "concept":
            term = item.get("term", "").strip()
            if not term: continue
            counters["concept"] = counters.get("concept", 0) + 1
            cid = f"{doc_id}_c{counters['concept']}"
            concept_terms[term] = cid
            entries.append(_make_entry(item, "concept", doc_id, counters, concept_terms))
        else:
            entries.append(_make_entry(item, t, doc_id, counters, concept_terms))
    return [e for e in entries if e is not None]


def build_output(meta_from_preprocess: dict, kg_parsed: dict, doc_id: str, model: str) -> dict:
    """组装最终输出: metadata 来自 preprocess，entries 来自 LLM 知识抽取。"""
    metadata = {
        "doc_id": doc_id,
        "source_file": meta_from_preprocess.get("source_file", ""),
        "title": meta_from_preprocess.get("title"),
        "year": meta_from_preprocess.get("year"),
        "doi": meta_from_preprocess.get("doi"),
        "abstract": meta_from_preprocess.get("abstract", ""),
        "introduction": meta_from_preprocess.get("introduction", ""),
        "primary_discipline": meta_from_preprocess.get("primary_discipline", {"level1": None, "level2": None, "level3": None}),
        "secondary_disciplines": meta_from_preprocess.get("secondary_disciplines", []),
        "keywords": meta_from_preprocess.get("keywords", []),
        "extraction_info": {"extraction_model": model, "extraction_timestamp": datetime.now(timezone.utc).isoformat()},
    }
    counters, concept_terms = {}, {}
    kg_entries = kg_parsed.get("entries")
    if kg_entries:
        entries = build_entries(kg_entries, doc_id, counters, concept_terms)
    else:
        flat = []
        for key, items in kg_parsed.items():
            mapped = GROUP_KEYS.get(key, key)
            if isinstance(items, list):
                for item in items:
                    item["type"] = mapped
                    flat.append(item)
        entries = build_entries(flat, doc_id, counters, concept_terms)
    return {"metadata": metadata, "entries": entries}


# ─── 抽取主逻辑 ─────────────────────────────────────────────

def load_meta(stem: str) -> dict | None:
    """从 kg_output/ 读取 preprocess 写入的结果。"""
    out_path = OUTPUT_DIR / f"{stem}.json"
    if not out_path.exists():
        return None
    return json.loads(out_path.read_text(encoding="utf-8"))


def extract_one(md_path, client, model, max_input_chars, temperature, debug, stream, max_output_tokens=16384, max_retries=5):
    """对单个 MD 文件做知识抽取。metadata 从 kg_output/ 读取，不重复调 LLM。"""
    raw_text = md_path.read_text(encoding="utf-8")
    orig_len = len(raw_text)
    debug_info = {"original_length": orig_len, "operations": [], "llm_responses": {}}
    token_usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}

    # 截断超长文本
    text = raw_text
    if len(text) > max_input_chars:
        debug_info["operations"].append({"action": "hard_truncate", "from_length": len(text), "to_length": max_input_chars})
        text = text[:max_input_chars]
    debug_info["processed_length"] = len(text)
    if debug: debug_info["processed_text"] = text

    # 读取 preprocess 结果（格式为 {"metadata": {...}, "entries": []}）
    file_data = load_meta(md_path.stem)
    if not file_data:
        print(f"  ⚠ 未找到 kg_output/{md_path.stem}.json，请先运行 kg_preprocess.py")
        return None, debug_info, token_usage
    meta = file_data.get("metadata", file_data)
    doc_id = meta.get("doc_id") or generate_doc_id(meta.get("title"), md_path.stem)

    # 调 LLM: 知识抽取（只调这一次）
    print(f"  字符: {orig_len:,} → 输入 {len(text):,}")
    sys_e, user_e = build_extraction_prompt(text)
    kg, raw_resp, usage = call_llm(client, model, sys_e, user_e, temperature, stream, max_output_tokens, max_retries=max_retries)
    token_usage["prompt_tokens"] += usage.get("prompt_tokens", 0)
    token_usage["completion_tokens"] += usage.get("completion_tokens", 0)
    token_usage["total_tokens"] += usage.get("total_tokens", 0)
    if debug: debug_info["llm_responses"]["extraction"] = raw_resp

    try: kg = LLMExtractionResponse(**kg).model_dump()
    except Exception: pass

    # 只补充 entries，metadata 原样保留
    counters, concept_terms = {}, {}
    kg_entries = kg.get("entries")
    if kg_entries:
        entries = build_entries(kg_entries, doc_id, counters, concept_terms)
    else:
        flat = []
        for key, items in kg.items():
            mapped = GROUP_KEYS.get(key, key)
            if isinstance(items, list):
                for item in items:
                    item["type"] = mapped
                    flat.append(item)
        entries = build_entries(flat, doc_id, counters, concept_terms)

    file_data["entries"] = entries
    file_data["metadata"]["extraction_info"] = {
        "extraction_model": model,
        "extraction_timestamp": datetime.now(timezone.utc).isoformat(),
    }
    result = file_data
    tc = {}
    for e in result["entries"]: tc[e["type"]] = tc.get(e["type"], 0) + 1
    print(f"  有效条目: {len(result['entries'])} 条")
    for t, c in tc.items(): print(f"    - {t}: {c}")
    print(f"  Token: {token_usage['total_tokens']} (输入 {token_usage['prompt_tokens']}, 输出 {token_usage['completion_tokens']})")
    return result, debug_info, token_usage


def collect_md_files(args):
    if args:
        files = []
        for name in args:
            p = Path(name)
            if not p.is_absolute():
                if (MARKDOWN_DIR / p).exists():
                    p = MARKDOWN_DIR / p
                elif not p.exists():
                    print(f"文件不存在: {name}")
                    continue
            if p.is_dir(): files.extend(sorted(p.glob("**/*.md")))
            elif p.is_file(): files.append(p)
        return files
    return sorted(MARKDOWN_DIR.glob("**/*.md"))


def main():
    logging.basicConfig(level=logging.WARNING, format="%(asctime)s %(levelname)s %(message)s")
    OUTPUT_DIR.mkdir(exist_ok=True)
    cfg = load_config()
    if not cfg["api_key"]: print("错误: 未设置 OPENAI_API_KEY"); return

    client = OpenAI(api_key=cfg["api_key"], base_url=cfg["base_url"] or None)
    force = "--force" in sys.argv
    debug = "--debug" in sys.argv
    stream = "--stream" in sys.argv
    reset_failed = "--reset-failed" in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if debug: DEBUG_DIR.mkdir(exist_ok=True)

    workers = cfg["workers"]
    if workers > 1 and stream:
        print("⚠ 并发模式下自动关闭 --stream")
        stream = False

    # 初始化状态库
    from kg_state import StateDB
    db = StateDB()
    if reset_failed:
        db.reset_failed("extract")

    # 注册所有 MD 文件
    md_files = collect_md_files(args)
    if not md_files: print("没有找到 MD 文件"); return
    db.register_files([p.stem for p in md_files])
    db.print_stats()

    def _worker():
        """单个工作线程：循环领取任务直到没有任务为止。"""
        while True:
            stem = db.claim_one("extract")
            if stem is None:
                break
            md_path = MARKDOWN_DIR / f"{stem}.md"
            if not md_path.exists():
                # 子目录里找
                matches = list(MARKDOWN_DIR.glob(f"**/{stem}.md"))
                if not matches:
                    db.mark_failed(stem, "extract", "MD 文件不存在")
                    continue
                md_path = matches[0]

            print(f"[抽取] {stem}")
            try:
                result, dbg, tokens = extract_one(
                    md_path, client, cfg["model"], cfg["max_input_chars"],
                    cfg["temperature"], debug, stream, cfg["max_output_tokens"],
                    max_retries=cfg["max_retries"])
                if result is None:
                    db.mark_failed(stem, "extract", "preprocess 结果不存在")
                    continue

                out_path = OUTPUT_DIR / f"{stem}.json"
                out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

                if debug:
                    if dbg.get("processed_text"):
                        (DEBUG_DIR / f"{stem}_processed.md").write_text(dbg["processed_text"], encoding="utf-8")
                    if dbg["llm_responses"].get("extraction"):
                        (DEBUG_DIR / f"{stem}_llm_extraction.json").write_text(dbg["llm_responses"]["extraction"], encoding="utf-8")

                db.mark_done(stem, "extract")
                db.set_extract_model(stem, cfg["model"])
                print(f"  ✓ {stem}: {len(result['entries'])} 条  token={tokens.get('total_tokens', 0)}")
            except Exception as e:
                db.mark_failed(stem, "extract", str(e))
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
