"""
kg_prompts.py — 论文知识抽取的 prompt 模板

学科分类 prompt: 传入 abstract+intro（或前N字符），LLM 输出 title/year/doi + 学科 + keywords
知识抽取 prompt: 传入论文全文，LLM 输出 10 类知识条目
"""

import json

LEVEL1_DISCIPLINES = [
    "数学", "信息科学与系统科学", "力学", "物理学", "化学",
    "天文学", "地球科学", "生物学", "农学", "林学",
    "畜牧、兽医科学", "水产学", "基础医学", "临床医学", "预防医学与卫生学",
    "军事医学与特种医学", "药学", "中医学与中药学", "工程与技术科学基础学科", "测绘科学技术",
    "材料科学", "矿山工程技术", "冶金工程技术", "机械工程", "动力与电气工程",
    "能源科学技术", "核科学技术", "电子、通信与自动控制技术", "计算机科学技术", "化学工程",
    "纺织科学技术", "食品科学技术", "土木建筑工程", "水利工程", "交通运输工程",
    "航空、航天科学技术", "环境科学技术", "安全科学技术", "管理学", "经济学",
    "政治学", "法学", "军事学", "社会学", "民族学",
    "新闻学与传播学", "图书馆、情报与文献学", "教育学", "体育科学", "统计学",
]
LEVEL1_DISCIPLINES_TEXT = "、".join(LEVEL1_DISCIPLINES)

# ─── 知识抽取输出示例 ───────────────────────────────────────

OUTPUT_EXAMPLE = {
    "entries": [
        {"type": "concept", "concept_id": "doc_xxx_c1", "term": "high-entropy alloy", "normalized": "高熵合金",
         "std_label": "HEA", "evidence": {"section": "Abstract", "original_text": "We reveal that high-entropy alloys (HEAs) can efficiently activate the LOM through synergistic multi-path electron transfer."},
         "confidence": 0.96},
        {"type": "concept", "concept_id": "doc_xxx_c2", "term": "oxygen evolution reaction", "normalized": "氧析出反应",
         "std_label": "OER", "evidence": {"section": "Abstract", "original_text": "Electrocatalytic oxygen evolution reaction (OER) is key to several energy technologies but suffers from low activity."},
         "confidence": 0.98},
        {"type": "relation", "relation_id": "doc_xxx_r1", "head": "high-entropy alloy",
         "relation_type": "enhances", "relation_surface": "can efficiently activate",
         "tail": "oxygen evolution reaction",
         "evidence": {"section": "Abstract", "original_text": "We reveal that high-entropy alloys (HEAs) can efficiently activate the LOM for enhanced oxygen evolution activity."},
         "confidence": 0.93},
        {"type": "dataset", "dataset_id": "doc_xxx_d1", "name": "OER activity benchmark", "samples": None, "domain": "electrochemistry",
         "evidence": {"section": "Results", "original_text": "We benchmark our HEA against state-of-the-art OER catalysts including IrO2 and RuO2."},
         "confidence": 0.90},
        {"type": "method", "method_id": "doc_xxx_m1", "name": "Raman spectroscopy", "method_type": "instrument",
         "evidence": {"section": "Methods", "original_text": "We analyzed the catalyst surface using Raman spectroscopy following the i-t tests in both KOH and TMAOH solutions."},
         "confidence": 0.95},
        {"type": "experiment", "experiment_id": "doc_xxx_x1", "task": "electrochemical stability test",
         "evidence": {"section": "Methods", "original_text": "All electrochemical measurements were performed at 298 K under ambient pressure using a standard three-electrode configuration."},
         "confidence": 0.95},
        {"type": "performance_result", "perf_id": "doc_xxx_p1",
         "evidence": {"section": "Results", "original_text": "The FeCoNiCrMn HEA exhibits a low overpotential of 280 mV at 10 mA/cm², outperforming IrO2 (320 mV) and RuO2 (310 mV)."},
         "confidence": 0.95},
        {"type": "claim", "claim_id": "doc_xxx_ca1",
         "evidence": {"section": "Abstract", "original_text": "Configurational entropy in high-entropy alloys synergistically activates multiple electron transfer pathways, enabling superior OER performance."},
         "confidence": 0.96},
        {"type": "conclusion", "conclusion_id": "doc_xxx_cl1",
         "evidence": {"section": "Conclusion", "original_text": "High-entropy alloys enable multi-path electron transfer to synergistically activate the lattice oxygen mechanism, providing a new design strategy for efficient OER catalysts."},
         "confidence": 0.96},
        {"type": "limitation", "limitation_id": "doc_xxx_lm1",
         "evidence": {"section": "Discussion", "original_text": "The current study is limited to five-component HEAs in alkaline media; generalizability to acid-stable compositions remains to be demonstrated."},
         "confidence": 0.92},
        {"type": "future_work", "future_work_id": "doc_xxx_fw1",
         "evidence": {"section": "Discussion", "original_text": "Future studies should explore HEAs in other electrocatalytic reactions such as CO2 reduction and nitrogen reduction."},
         "confidence": 0.93},
    ]
}
OUTPUT_EXAMPLE_JSON = json.dumps(OUTPUT_EXAMPLE, ensure_ascii=False, indent=2)

# ─── 学科分类 + Metadata 修正 Prompt ──────────────────────────

DISCIPLINE_SYSTEM_PROMPT = """你是一位学术论文元数据分析专家。根据提供的论文内容，完成两个任务：
1. 审查并修正论文元数据（标题、年份、DOI）
2. 判断学科归属

## 一级学科列表（level1 必须从中选择）

{discipline_list}

## 正则预提取结果

以下是通过正则自动提取的元数据，可能存在错误（如标题误识别为期刊名、年份不正确等），请根据论文内容审查修正：
- 预提取标题: {regex_title}
- 预提取年份: {regex_year}
- 预提取DOI: {regex_doi}

## 输出格式

```json
{{
  "title": "论文完整标题",
  "year": 2026,
  "doi": "10.xxxx/xxxxx 或 null",
  "primary_discipline": {{"level1": "一级学科名称", "level2": "二级学科名称", "level3": "三级学科名称"}},
  "secondary_disciplines": {{"level1": "一级学科名称", "level2": "二级学科名称", "level3": "三级学科名称"}},
  "keywords": ["keyword1", "keyword2", "keyword3"]
}}
```

## 要求

1. **title**：论文的完整标题。如果预提取标题是期刊名、版权声明、作者列表等，必须从论文内容中找到真正的论文标题
2. **year**：论文发表年份。从版权信息(©)、Published/Date/Accepted 字段推断，如果预提取年份明显不合理请修正
3. **doi**：DOI 编号，找不到则填 null
4. **primary_discipline 必填**：level1 必须从上述列表中选择，level2/level3 无法确定则填 null
5. **secondary_disciplines**：仅当论文明确涉及其他学科时才填写，否则填 null
6. **keywords**：3-5 个最相关的英文关键词，使用原文术语"""

DISCIPLINE_USER_PROMPT_TEMPLATE = """## 论文内容

{paper_content}

请审查修正元数据并输出学科分类和关键词。"""

# ─── 知识抽取 Prompt ─────────────────────────────────────────

EXTRACTION_SYSTEM_PROMPT = """你是一位科学文献知识抽取专家。从学术论文中提取结构化知识。

## 输出格式

```json
{output_example}
```

## 10 种知识类型

1. **concept**: 关键概念、术语、实体（term/normalized/std_label）
2. **relation**: 概念间语义关系（head/tail 必须对应已抽取的 concept term）
3. **dataset**: 论文使用/产生的数据集（name/samples/domain）
4. **method**: 方法、模型、算法、仪器（name/method_type）
5. **experiment**: 实验设置与流程（task）
6. **performance_result**: 性能指标（仅 evidence）
7. **conclusion**: 核心结论（仅 evidence）
8. **claim**: 核心主张/发现（仅 evidence）
9. **future_work**: 未来研究方向（仅 evidence）
10. **limitation**: 方法局限、适用约束（仅 evidence）

## 提取原则

1. **忠实性**：original_text 必须是原文直接摘录，禁止改写
2. **完整性**：original_text 包含 3-6 个完整句子，保留充分上下文
3. **关联性**：relation 的 head/tail 必须对应已抽取的 concept term
4. **轻标注**：concept/dataset/method/experiment 的字段值简短
5. **覆盖度**：每篇论文 20-50 条记录；concept 10-20 条，relation 5-10 条，其他类型按实际分布
6. **claim/conclusion/limitation/future_work** 不是每篇都有，按实际内容抽取"""

EXTRACTION_USER_PROMPT_TEMPLATE = """## 论文内容

{paper_text}

请提取知识条目。"""


# ─── Prompt 构建函数 ────────────────────────────────────────

def build_discipline_prompt(abstract: str, introduction: str, paper_head: str,
                            regex_title: str, regex_year, regex_doi) -> tuple[str, str]:
    """构建学科分类+metadata修正 prompt。

    优先使用 abstract+introduction，缺失则用 paper_head（论文前N字符）。
    regex_title/year/doi 传入正则预提取结果，让 LLM 审查修正。
    """
    if abstract or introduction:
        content_parts = []
        if abstract:
            content_parts.append(f"### Abstract\n\n{abstract}")
        if introduction:
            content_parts.append(f"### Introduction\n\n{introduction}")
        paper_content = "\n\n".join(content_parts)
    else:
        paper_content = paper_head or "无内容"

    sys_prompt = DISCIPLINE_SYSTEM_PROMPT.format(
        discipline_list=LEVEL1_DISCIPLINES_TEXT,
        regex_title=regex_title or "未提取到",
        regex_year=str(regex_year) if regex_year else "未提取到",
        regex_doi=regex_doi or "未提取到",
    )
    user_prompt = DISCIPLINE_USER_PROMPT_TEMPLATE.format(paper_content=paper_content)
    return sys_prompt, user_prompt


def build_extraction_prompt(paper_text: str) -> tuple[str, str]:
    return (EXTRACTION_SYSTEM_PROMPT.format(output_example=OUTPUT_EXAMPLE_JSON),
            EXTRACTION_USER_PROMPT_TEMPLATE.format(paper_text=paper_text))
