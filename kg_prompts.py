"""
kg_prompts.py — 论文知识抽取的 prompt 模板

8 种知识类型:
1. concept - 概念
2. relation - 关系
3. dataset_and_benchmark - 数据集与基准
4. method_and_experiment - 方法与实验
5. performance_result - 性能结果
6. experimental_parameter - 实验参数与物理量
7. data_specification - 数据规范与标准
8. conclusion_and_insight - 结论与洞见
"""

import json

# ─── 一级学科列表（从 disciplines.json 提取）──────────────────────

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

# ─── 输出示例（符合 schema.md 格式）──────────────────────────────

OUTPUT_EXAMPLE = {
    "entries": [
        {
            "type": "concept",
            "term": "Oxygen evolution reaction",
            "normalized": "氧析出反应",
            "std_label": "OER",
            "evidence": {
                "section": "Abstract",
                "original_text": "Electrocatalytic oxygen evolution reaction (OER) is key to several energy technologies but suffers from low activity. Here we report that high-entropy alloys can efficiently activate the lattice oxygen mechanism for enhanced OER performance."
            },
            "confidence": 0.95
        },
        {
            "type": "concept",
            "term": "high-entropy alloy",
            "normalized": "高熵合金",
            "std_label": "HEA",
            "evidence": {
                "section": "Abstract",
                "original_text": "We reveal that high-entropy alloys (HEAs) can efficiently activate the LOM through synergistic multi-path electron transfer for enhanced oxygen evolution activity. The FeCoNiCrMn HEA exhibits a low overpotential of 280 mV at a current density of 10 mA/cm²."
            },
            "confidence": 0.96
        },
        {
            "type": "relation",
            "head": "high-entropy alloy",
            "head_term": "high-entropy alloy",
            "relation_type": "enhances",
            "relation_surface": "can efficiently activate",
            "tail": "oxygen evolution reaction",
            "tail_term": "oxygen evolution reaction",
            "direction": "directed",
            "evidence": {
                "section": "Abstract",
                "original_text": "We reveal that high-entropy alloys (HEAs) can efficiently activate the LOM through synergistic multi-path electron transfer for enhanced oxygen evolution activity. The multi-path electron transfer mechanism was confirmed by in-situ Raman spectroscopy."
            },
            "confidence": 0.93
        },
        {
            "type": "dataset_and_benchmark",
            "datasets": [
                {
                    "name": "FreeSolv",
                    "role": "used",
                    "samples": 642,
                    "domain": "chemistry",
                    "data_format": "SMILES",
                    "task_type": "regression"
                }
            ],
            "evidence": {
                "section": "Section 2",
                "original_text": "We evaluate our model on the FreeSolv dataset, which contains 642 small molecules with experimental solvation free energies. The dataset was split using scaffold splitting with 80% for training, 10% for validation, and 10% for testing."
            },
            "confidence": 0.93
        },
        {
            "type": "method_and_experiment",
            "methods": [
                {
                    "name": "D-MPNN",
                    "method_type": "model",
                    "category": "GNN"
                }
            ],
            "experiment": {
                "task": "molecular property prediction",
                "dataset_ref": "FreeSolv",
                "method_ref": "D-MPNN"
            },
            "evidence": {
                "section": "Methods",
                "original_text": "We employ D-MPNN (Directed Message Passing Neural Network) for molecular property prediction. The model takes molecular graphs as input and learns representations through message passing along directed edges. All models were trained for 100 epochs with learning rate 0.001."
            },
            "confidence": 0.93
        },
        {
            "type": "performance_result",
            "metrics": [
                {
                    "name": "RMSE",
                    "value": 1.15,
                    "unit": "kcal/mol",
                    "method_ref": "D-MPNN",
                    "dataset_ref": "FreeSolv"
                }
            ],
            "evidence": {
                "section": "Table 2",
                "original_text": "Our model achieves an RMSE of 1.15 kcal/mol on the FreeSolv benchmark with scaffold split, outperforming previous baselines including MPNN (1.34 kcal/mol) and SchNet (1.22 kcal/mol). The improvement is attributed to the directed message passing mechanism."
            },
            "confidence": 0.93
        },
        {
            "type": "experimental_parameter",
            "parameters": [
                {
                    "name": "temperature",
                    "value": 298,
                    "unit": "K",
                    "param_type": "env_condition"
                }
            ],
            "evidence": {
                "section": "Methods",
                "original_text": "All electrochemical measurements were performed at 298 K under ambient pressure using a standard three-electrode configuration. The electrolyte was 1.0 M KOH solution prepared with deionized water."
            },
            "confidence": 0.95
        },
        {
            "type": "data_specification",
            "spec_type": "format_rule",
            "related_formats": ["SMILES", "SDF"],
            "related_domain": "chemistry",
            "evidence": {
                "section": "Section 2.1",
                "original_text": "All molecular structures are represented in SMILES format following the Daylight specification. For 3D conformer generation, we used RDKit with the ETKDG algorithm. Structures with more than 50 heavy atoms were excluded from the dataset."
            },
            "confidence": 0.93
        },
        {
            "type": "conclusion_and_insight",
            "insight_type": "limitation",
            "evidence": {
                "section": "Discussion",
                "original_text": "Our approach currently struggles with molecules containing more than 50 heavy atoms, which we identify as a key limitation for future work. The message passing mechanism becomes computationally expensive for large molecules, and we plan to explore hierarchical approaches in future studies."
            },
            "confidence": 0.93
        }
    ]
}

OUTPUT_EXAMPLE_JSON = json.dumps(OUTPUT_EXAMPLE, ensure_ascii=False, indent=2)


# ─── 学科分类 Prompt ──────────────────────────────────────────────

DISCIPLINE_SYSTEM_PROMPT = """你是一位学术论文分类专家。根据论文的摘要和引言，判断该论文的学科归属。

## 一级学科列表（level1 必须从中选择）

{discipline_list}

## 输出格式

```json
{{
  "primary_discipline": {{
    "level1": "一级学科名称",
    "level2": "二级学科名称",
    "level3": "三级学科名称"
  }},
  "secondary_disciplines": null,
  "keywords": ["keyword1", "keyword2", "keyword3"]
}}
```

## 要求

1. **primary_discipline 必填**：论文的主学科，必须包含 level1/level2/level3
   - level1 必须从上述列表中选择
   - level2/level3 根据论文内容推断，如果无法确定填 null

2. **secondary_disciplines 辅助学科**：
   - 只有当论文明确涉及其他学科时才填写
   - 如果不涉及其他学科，填 null
   - 必须忠实于原文，不要猜测

3. **keywords 关键词**：
   - 选择 3-5 个最相关的英文关键词
   - 使用原文中的术语，不要翻译"""

DISCIPLINE_USER_PROMPT_TEMPLATE = """## 摘要

{abstract}

## 引言

{introduction}

请输出学科分类和关键词。"""


# ─── 主抽取 Prompt ───────────────────────────────────────────────

EXTRACTION_SYSTEM_PROMPT = """你是一位科学文献知识抽取专家。你的任务是从学术论文中提取结构化知识。

## 输出格式

```json
{output_example}
```

## 8 种知识类型

1. **concept**: 论文中的关键概念、术语、实体
2. **relation**: 概念之间的语义关系（head/tail 必须对应已抽取的 concept term）
3. **dataset_and_benchmark**: 论文使用/产生的数据集
4. **method_and_experiment**: 论文使用的方法、模型、实验设置
5. **performance_result**: 模型/方法的性能指标
6. **experimental_parameter**: 实验参数、物理量、条件
7. **data_specification**: 数据格式规范、标准
8. **conclusion_and_insight**: 结论、局限性、未来方向

## 提取原则

1. **忠实性**：original_text 必须是原文的直接摘录，禁止改写或编造
2. **完整性**：**original_text 范围要足够大**，包含 3-6 个完整句子，保留充分上下文让读者能快速定位原文
3. **关联性**：relation 的 head/tail 必须对应已抽取的 concept 的 term
4. **轻标注**：字段值简短，用短语而非完整句子
5. **覆盖度**：**每篇论文需要提取 20-50 条记录**，覆盖所有 8 种类型
6. **必填字段**：每条记录必须包含 type 和 evidence

**original_text 示例对比**：
- ❌ 太短：`"5.0 sigma"` — 缺少上下文，难以定位
- ❌ 太短：`"The threshold is 5.0."` — 缺少背景信息
- ✅ 合适：完整段落，包含条件、数值、单位和意义说明

上述示例仅展示格式，实际提取时需要更全面地覆盖论文内容。"""

EXTRACTION_USER_PROMPT_TEMPLATE = """## 论文内容

{paper_text}

请提取知识条目。"""


# ─── Prompt 构建函数 ───────────────────────────────────────────────

def build_discipline_prompt(abstract: str, introduction: str) -> tuple[str, str]:
    """构建学科分类 prompt，返回 (system_prompt, user_prompt)。"""
    system_prompt = DISCIPLINE_SYSTEM_PROMPT.format(discipline_list=LEVEL1_DISCIPLINES_TEXT)
    user_prompt = DISCIPLINE_USER_PROMPT_TEMPLATE.format(
        abstract=abstract or "无摘要",
        introduction=introduction or "无引言"
    )
    return system_prompt, user_prompt


def build_extraction_prompt(paper_text: str) -> tuple[str, str]:
    """构建主抽取 prompt，返回 (system_prompt, user_prompt)。"""
    system_prompt = EXTRACTION_SYSTEM_PROMPT.format(output_example=OUTPUT_EXAMPLE_JSON)
    user_prompt = EXTRACTION_USER_PROMPT_TEMPLATE.format(paper_text=paper_text)
    return system_prompt, user_prompt