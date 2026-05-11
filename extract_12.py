"""
extract_12.py — 分组并行知识抽取：读 MD + 读 preprocess 结果 → 4 组并行 LLM → 合并写 kg_output

与 kg_extract.py 的区别：
  - 将 12 种知识类型拆分为 4 组，每组独立调 LLM 并行抽取
  - Group1: concept + relation
  - Group2: dataset + method + data_specification
  - Group3: experiment + quantitative_result + performance_result
  - Group4: conclusion + future_work + limitation + claim
  - 每组调用各有专业 prompt，提升抽取质量和召回率

输入: markdown/*.md + kg_output/*.json (preprocess 结果)
输出: kg_output/*.json (entries 来自 4 组并行 LLM 抽取)
"""

import json
import os
import re
import sys
import time
import random
import logging
import hashlib
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

from openai import OpenAI, RateLimitError, APIConnectionError, APITimeoutError
from dotenv import load_dotenv

from kg_prompts import build_grouped_extraction_prompts
from kg_schema import LLMExtractionResponse

load_dotenv()
logger = logging.getLogger(__name__)
BASE_DIR = Path(__file__).parent
MARKDOWN_DIR = BASE_DIR / "markdown"
OUTPUT_DIR = BASE_DIR / "kg_output"
DEBUG_DIR = OUTPUT_DIR / "debug"

TYPE_META = {
    "concept":             {"prefix": "c",  "id_field": "concept_id"},
    "relation":            {"prefix": "r",  "id_field": "relation_id"},
    "dataset":             {"prefix": "d",  "id_field": "dataset_id"},
    "method":              {"prefix": "m",  "id_field": "method_id"},
    "experiment":          {"prefix": "x",  "id_field": "experiment_id"},
    "performance_result":  {"prefix": "p",  "id_field": "perf_id"},
    "quantitative_result": {"prefix": "qr", "id_field": "qr_id"},
    "data_specification":  {"prefix": "ds", "id_field": "ds_id"},
    "conclusion":          {"prefix": "cl", "id_field": "conclusion_id"},
    "claim":               {"prefix": "ca", "id_field": "claim_id"},
    "future_work":         {"prefix": "fw", "id_field": "future_work_id"},
    "limitation":          {"prefix": "lm", "id_field": "limitation_id"},
}
TYPE_FIELDS = {
    "concept": ["term", "normalized", "std_label"],
    "relation": ["head", "relation_type", "relation_surface", "tail"],
    "dataset": ["name", "modality", "domain"],
    "method": ["name", "method_type"],
    "experiment": ["task", "setup"],
    "quantitative_result": ["quantity", "value", "unit", "context", "result_type"],
    "data_specification": ["spec_type", "description"],
    "performance_result": ["metric", "compared_to"],
}
GROUP_KEYS = {
    "concepts": "concept", "relations": "relation", "datasets": "dataset",
    "methods": "method", "experiments": "experiment", "performances": "performance_result",
    "quantitative_results": "quantitative_result", "data_specifications": "data_specification",
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


def _repair_truncated_json(raw: str) -> str:
    """修复因 token 截断导致的不完整 JSON。

    策略：从末尾逐步删除字符，每次尝试补全数组/对象闭合，
    直到 JSON 可解析或剩余内容太少。
    """
    raw = raw.strip()
    # 去掉 markdown 代码标记
    for tag in ["```json", "```"]:
        if raw.endswith(tag):
            raw = raw[:-len(tag)].strip()
        if raw.startswith(tag):
            raw = raw[len(tag):].strip()

    # 方法1: 找到最后一个完整条目边界（条目间以 \n    { 或 ,\n    { 分隔）
    for sep in ['\n    {', '\n  {', '\n    "', '\n  "']:
        pos = raw.rfind(sep)
        if pos < 100:
            continue  # 太短，不切
        # 检查 pos 前后：前面应该是 }, 或 }，后面应该开始新条目
        before = raw[:pos].rstrip()
        if before.endswith(','):
            before = before[:-1].rstrip()
        if before.endswith('}'):
            candidate = before + '\n    ]\n  }'
            try:
                obj = json.loads(candidate)
                if isinstance(obj, dict) and 'entries' in obj:
                    return candidate
            except json.JSONDecodeError:
                continue

    # 方法2: 从末尾逐字符回退，找最后一个合法的完整值边界
    # 去掉末尾不完整的字符串或结构
    for cutoff in range(len(raw), max(len(raw) - 500, 50), -1):
        truncated = raw[:cutoff].rstrip()
        if truncated.endswith(','):
            truncated = truncated[:-1].rstrip()
        # 补全数组和对象
        for suffix in ['\n    ]\n  }', '\n  ]\n}', ']}', '] }']:
            candidate = truncated + suffix
            try:
                obj = json.loads(candidate)
                if isinstance(obj, dict) and 'entries' in obj:
                    return candidate
            except json.JSONDecodeError:
                continue

    return raw


def _sanitize(obj):
    if isinstance(obj, dict): return {k: _sanitize(v) for k, v in obj.items()}
    if isinstance(obj, list): return [_sanitize(x) for x in obj]
    if isinstance(obj, int) and not isinstance(obj, bool) and abs(obj) >= 10**1000:
        return str(obj)
    return obj


def call_llm(client, model, sys_prompt, user_prompt, temperature, stream=False, max_tokens=16384, max_retries=5):
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
            wait = 2 ** attempt + random.uniform(0, 1)
            logger.warning(f"限流 ({attempt+1}/{max_retries})，等待 {wait:.1f}s: {e}")
            if attempt == max_retries - 1: raise
            time.sleep(wait)
        except (APIConnectionError, APITimeoutError) as e:
            wait = 2 ** attempt
            logger.warning(f"网络错误 ({attempt+1}/{max_retries})，等待 {wait}s: {e}")
            if attempt == max_retries - 1: raise
            time.sleep(wait)
        except json.JSONDecodeError as e:
            # 尝试修复被 token 截断的 JSON（用 raw 原文，不要用 extracted）
            repaired = _repair_truncated_json(raw)
            if repaired != raw:
                try:
                    repaired_json = _extract_json(repaired)
                    start = next((i for i, c in enumerate(repaired_json) if c in "{["), 0)
                    obj, _ = json.JSONDecoder().raw_decode(repaired_json, start)
                    n_entries = len(obj.get('entries', []))
                    print(f"  ⚡ JSON 截断修复: 恢复 {n_entries} 条")
                    return _sanitize(obj), raw, usage
                except (json.JSONDecodeError, Exception) as e2:
                    logger.warning(f"JSON 修复失败 ({attempt+1}/{max_retries}): {e2}")
            else:
                logger.warning(f"JSON 解析错误 ({attempt+1}/{max_retries}), 无法修复: {e}")
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
            entry = _make_entry(item, "concept", doc_id, counters, concept_terms)
            if entry:
                concept_terms[term] = entry[TYPE_META["concept"]["id_field"]]
                entries.append(entry)
        else:
            entry = _make_entry(item, t, doc_id, counters, concept_terms)
            if entry: entries.append(entry)
    return entries


# ─── 分组并行提取核心逻辑 ─────────────────────────────────────

def extract_one_group(client, model, sys_prompt, user_prompt, temperature, max_tokens, max_retries, debug) -> tuple[list, str, dict]:
    """单组提取，返回 (entries_list, raw_response, token_usage)。"""
    kg, raw_resp, usage = call_llm(client, model, sys_prompt, user_prompt, temperature,
                                   stream=False, max_tokens=max_tokens, max_retries=max_retries)
    entries = []
    kg_entries = kg.get("entries")
    if kg_entries:
        entries = list(kg_entries)
    else:
        for key, items in kg.items():
            mapped = GROUP_KEYS.get(key, key)
            if isinstance(items, list):
                for item in items:
                    item["type"] = mapped
                    entries.append(item)
    return entries, raw_resp, usage


# 组名 → 在 entries 中对应的知识类型
GROUP_TYPE_MAP = {
    "G1_concept_relation":      ["concept", "relation"],
    "G2_dataset_spec":           ["dataset", "data_specification"],
    "G3_method_experiment":      ["method", "experiment"],
    "G4_quant_perf":             ["quantitative_result", "performance_result"],
    "G5_insight_outlook":        ["conclusion", "claim", "future_work", "limitation"],
}


def extract_one(md_path, client, model, max_input_chars, temperature, debug, stream,
                max_output_tokens=16384, max_retries=5, retry_groups: list[str] | None = None):
    """串行 4 组 LLM 调用，支持增量重提取。

    retry_groups=None: 全量提取 4 组
    retry_groups=[...]: 仅提取指定组，与已有 entries 合并
    """
    raw_text = md_path.read_text(encoding="utf-8")
    orig_len = len(raw_text)
    debug_info = {"original_length": orig_len, "groups": {}}
    token_usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}

    text = raw_text
    if len(text) > max_input_chars:
        text = text[:max_input_chars]
    debug_info["processed_length"] = len(text)

    out_path = OUTPUT_DIR / md_path.relative_to(MARKDOWN_DIR).with_suffix(".json")
    if not out_path.exists():
        out_path = OUTPUT_DIR / f"{md_path.stem}.json"
        if not out_path.exists():
            print(f"  ⚠ 未找到 preprocess 结果: {md_path.stem}")
            return None, None, debug_info, token_usage
    file_data = json.loads(out_path.read_text(encoding="utf-8"))
    meta = file_data.get("metadata", file_data)
    doc_id = meta.get("doc_id") or generate_doc_id(meta.get("title"), md_path.stem)

    # 判断是否增量模式
    is_retry = bool(retry_groups)
    if is_retry:
        existing_entries = file_data.get("entries", [])
        prev_failed = retry_groups
        print(f"  字符: {orig_len:,} → 输入 {len(text):,}  增量重提取 {prev_failed}")

    # 构建 4 组 prompt，只提取需要的组
    all_prompts = build_grouped_extraction_prompts(text)
    if is_retry:
        group_prompts = [(n, s, u) for n, s, u in all_prompts if n in retry_groups]
    else:
        group_prompts = all_prompts

    if not group_prompts:
        print(f"  ⚠ 没有需要提取的组")
        return None, None, debug_info, token_usage

    group_results = {}
    failed_groups = []
    t0 = time.time()
    for group_name, sys_e, user_e in group_prompts:
        prefix = "  [重试]" if is_retry else ""
        try:
            entries, raw_resp, usage = extract_one_group(
                client, model, sys_e, user_e, temperature,
                max_output_tokens, max_retries, debug)
            group_results[group_name] = entries
            token_usage["prompt_tokens"] += usage.get("prompt_tokens", 0)
            token_usage["completion_tokens"] += usage.get("completion_tokens", 0)
            token_usage["total_tokens"] += usage.get("total_tokens", 0)
            n = len(entries)
            print(f"    {prefix}[{group_name}] {n} 条  in={usage.get('prompt_tokens', 0)} out={usage.get('completion_tokens', 0)} total={usage.get('total_tokens', 0)}")
            if debug:
                debug_info["groups"][group_name] = {"entries": n, "raw": raw_resp}
        except Exception as e:
            failed_groups.append(group_name)
            group_results[group_name] = []
            print(f"    {prefix}[{group_name}] ✗ 失败: {e}")
            if debug:
                debug_info["groups"][group_name] = {"error": str(e)}

    elapsed = time.time() - t0
    status = f"  {len(failed_groups)} 组失败" if failed_groups else "全部成功"
    print(f"  提取完成: {elapsed:.1f}s  {status}")

    # 合并：增量模式下，先加载已有 entries，替换失败组的条目
    if is_retry:
        # 移除旧失败组的条目
        types_to_replace = set()
        for gn in retry_groups:
            types_to_replace.update(GROUP_TYPE_MAP.get(gn, []))
        kept_entries = [e for e in existing_entries if e["type"] not in types_to_replace]
        # 重建 counters 和 concept_terms（扫描保留的 concept 条目）
        counters, concept_terms = {}, {}
        for e in kept_entries:
            t = e["type"]
            counters[t] = counters.get(t, 0) + 1
            if t == "concept" and e.get("concept_id"):
                # concept term 可能不在 entry 里（field name 是 term 还是 concept_id）...
                # 我们需要 term→concept_id 映射。从 entry 的 term 和 concept_id 重建。
                term = e.get("term", "")
                if term:
                    concept_terms[term] = e["concept_id"]
    else:
        counters, concept_terms = {}, {}
        kept_entries = []

    # 对新提取的组 build_entries（共享 counters 和 concept_terms）
    new_entries = []
    for gn in ["G1_concept_relation", "G2_dataset_spec", "G3_method_experiment", "G4_quant_perf", "G5_insight_outlook"]:
        if gn in group_results:
            new_entries.extend(build_entries(group_results[gn], doc_id, counters, concept_terms))

    all_entries = kept_entries if is_retry else []
    all_entries.extend(new_entries)

    file_data["entries"] = all_entries
    file_data["metadata"]["extraction_info"] = {
        "extraction_model": model,
        "extraction_timestamp": datetime.now(timezone.utc).isoformat(),
        "extraction_method": "grouped_serial_5groups",
        "retry_groups": retry_groups if is_retry else None,
        "failed_groups": failed_groups if failed_groups else None,
    }
    result = file_data

    tc = {}
    for e in result["entries"]: tc[e["type"]] = tc.get(e["type"], 0) + 1
    print(f"  合计有效条目: {len(result['entries'])} 条")
    for t, c in sorted(tc.items()): print(f"    - {t}: {c}")
    print(f"  Token 总计: {token_usage['total_tokens']} "
          f"(输入 {token_usage['prompt_tokens']}, 输出 {token_usage['completion_tokens']})")
    return result, True if failed_groups else False, debug_info, token_usage


# ─── 文件收集 ────────────────────────────────────────────────

def collect_md_files(args):
    if args:
        files = []
        for name in args:
            p = Path(name)
            if not p.is_absolute():
                if (MARKDOWN_DIR / p).exists():
                    p = MARKDOWN_DIR / p
                elif p.exists():
                    p = p.resolve()
                else:
                    print(f"文件不存在: {name}")
                    continue
            if p.is_dir(): files.extend(sorted(p.glob("**/*.md")))
            elif p.is_file(): files.append(p)
        return files
    return sorted(MARKDOWN_DIR.glob("**/*.md"))


# ─── 主入口 ──────────────────────────────────────────────────

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

    from kg_state import StateDB, resolve_db_path
    _input_dir = None
    if args and len(args) == 1:
        _p = Path(args[0])
        if not _p.is_absolute() and (MARKDOWN_DIR / _p).is_dir():
            _input_dir = MARKDOWN_DIR / _p
        elif _p.is_dir():
            _input_dir = _p
    db = StateDB(resolve_db_path(_input_dir))
    if reset_failed:
        db.reset_failed("extract")

    md_files = collect_md_files(args)
    if not md_files: print("没有找到 MD 文件"); return
    db.register_files([p.stem for p in md_files])
    db.print_stats()

    if cfg["skip_existing"]:
        done = {s for s in db.get_processed("extract") if db.was_success(s, "extract")}
        md_files = [p for p in md_files if p.stem not in done]
        if not md_files:
            print("所有文件已完成，无需抽取")
            db.print_stats()
            return
        print(f"待处理: {len(md_files)} 个文件\n")

    if cfg["process_limit"] and cfg["process_limit"] > 0:
        md_files = md_files[:cfg["process_limit"]]

    def _worker():
        while True:
            stem = db.claim_one("extract")
            if stem is None: break
            # 检查是否为增量重试
            retry_groups = db.get_failed_groups(stem)
            md_path = MARKDOWN_DIR / f"{stem}.md"
            if not md_path.exists():
                matches = list(MARKDOWN_DIR.glob(f"**/{stem}.md"))
                if not matches:
                    db.mark_failed(stem, "extract", "MD 文件不存在")
                    continue
                md_path = matches[0]

            tag = f"[extract_12] {'Δ' if retry_groups else 'F'}"
            print(f"{tag} {stem}" + (f" 仅重试 {retry_groups}" if retry_groups else ""))
            try:
                result, had_failures, dbg, tokens = extract_one(
                    md_path, client, cfg["model"], cfg["max_input_chars"],
                    cfg["temperature"], debug, False, cfg["max_output_tokens"],
                    max_retries=cfg["max_retries"], retry_groups=retry_groups)
                if result is None:
                    db.mark_failed(stem, "extract", "preprocess 结果不存在")
                    continue

                out_path = OUTPUT_DIR / md_path.relative_to(MARKDOWN_DIR).with_suffix(".json")
                out_path.parent.mkdir(parents=True, exist_ok=True)
                out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

                if debug and dbg:
                    for gname, ginfo in dbg.get("groups", {}).items():
                        if ginfo.get("raw"):
                            (DEBUG_DIR / f"{stem}_{gname}_raw.json").write_text(
                                ginfo["raw"], encoding="utf-8")

                # 全成功 → done；有失败 → partial 并记录失败组
                if had_failures:
                    failed = result["metadata"]["extraction_info"]["failed_groups"]
                    db.set_extract_failed_groups(stem, failed)
                    db.set_extract_model(stem, cfg["model"],
                        prompt_tokens=tokens.get("prompt_tokens", 0),
                        completion_tokens=tokens.get("completion_tokens", 0))
                    print(f"  ⚡ {stem}: {len(result['entries'])} 条  {len(failed)}组失败等待重试  token={tokens.get('total_tokens', 0)}")
                else:
                    db.mark_done(stem, "extract")
                    db.set_extract_model(stem, cfg["model"],
                        prompt_tokens=tokens.get("prompt_tokens", 0),
                        completion_tokens=tokens.get("completion_tokens", 0))
                    print(f"  ✓ {stem}: {len(result['entries'])} 条  token={tokens.get('total_tokens', 0)}")
            except Exception as e:
                db.mark_failed(stem, "extract", str(e))
                print(f"  ✗ {stem}: {e}")

    if workers == 1:
        _worker()
    else:
        print(f"并发模式: {workers} 个工作线程（论文间并行，论文内 4 组串行）\n")
        with ThreadPoolExecutor(max_workers=workers) as pool:
            futures = [pool.submit(_worker) for _ in range(workers)]
            for f in as_completed(futures):
                if f.exception():
                    print(f"工作线程异常: {f.exception()}")

    db.print_stats()


if __name__ == "__main__":
    main()
