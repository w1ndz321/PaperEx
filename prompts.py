"""
prompts.py — 论文知识抽取的 prompt 模板

8种知识类型: claim, concept, method, dataset, evaluation_strategy, metric, result, assumption
"""

KNOWLEDGE_TYPES = {
    "claim":               "论文的核心断言或主要论点。例如：'iGFT 在低资源场景下显著优于基线方法'",
    "concept":             "论文定义或使用的关键概念、术语、理论框架。例如：'密集检索是指用向量相似度匹配查询与文档'",
    "method":              "论文提出或使用的方法、算法、技术路线。例如：'三阶段 Generation-Filtering-Tuning 框架'",
    "dataset":             "论文涉及的数据集，包括名称、规模、来源。例如：'MS MARCO 包含约100万个查询'",
    "evaluation_strategy": "评估设计，包括实验设置、基准选取、对比方法。例如：'与 BM25、DPR 等6个基线在4个数据集上对比'",
    "metric":              "评估指标的定义或具体数值。例如：'MRR@10 = 0.387，超越基线 3.2 个百分点'",
    "result":              "实验结论或量化结果。例如：'在低资源设置下，iGFT 的 NDCG@10 提升 5.1%'",
    "assumption":          "论文成立所依赖的前提或假设。例如：'假设少量标注数据足以微调生成器'",
}


SYSTEM_PROMPT = """你是一位科学文献知识抽取专家。你的任务是从学术论文中提取结构化知识条目。

你需要提取以下8种类型的知识：

1. **claim** — 论文的核心断言或主要论点
2. **concept** — 关键概念、术语、理论框架的定义
3. **method** — 论文提出或使用的方法、算法、技术路线
4. **dataset** — 数据集的名称、规模、来源、特征
5. **evaluation_strategy** — 评估设计，包括实验设置、基准选取、对比方法
6. **metric** — 评估指标的定义或具体数值
7. **result** — 实验结论或量化结果
8. **assumption** — 论文成立所依赖的前提或假设

## 提取原则

- **忠实性**：text 字段必须是原文的直接摘录或极近似转述，不得编造
- **完整性**：尽量覆盖论文的主要知识点，不要遗漏重要信息
- **具体性**：包含具体数值、名称、公式等，避免空泛描述

## 输出格式

返回严格的 JSON，格式如下：

```json
{
  "entries": [
    {
      "type": "claim|concept|method|dataset|evaluation_strategy|metric|result|assumption",
      "text": "原文对应内容的直接摘录或极近似转述",
      "normal_text": "轻量标准化后的表述：统一术语、修正语法、去除冗余，但保留核心语义",
      "topic_tags": ["主题关键词1", "主题关键词2"],
      "confidence": 0.9,
      "source_evidence": "该知识在原文中的位置，如章节标题或上下文片段"
    }
  ]
}
```

字段说明：
- **type**：必填，只能是上述8种之一
- **text**：必填，原文内容，保持原文措辞
- **normal_text**：必填，标准化表述，便于跨文献比较和检索
- **topic_tags**：必填，2-5个能代表该条知识主题的关键词
- **confidence**：必填，0.0-1.0，对该条知识准确性和完整性的信心
- **source_evidence**：必填，指出该知识来自原文的哪个位置（章节名、段落首句等）"""


USER_PROMPT_TEMPLATE = """请从以下学术论文中提取结构化知识。

## 论文内容

{paper_text}

## 要求

1. 提取论文中所有重要的 claim、concept、method、dataset、evaluation_strategy、metric、result、assumption
2. text 字段必须忠实于原文，normal_text 做轻量标准化
3. 只输出 JSON，不要输出其他内容"""


def build_prompt(paper_text: str) -> tuple[str, str]:
    """构建抽取 prompt，返回 (system_prompt, user_prompt)。"""
    user_prompt = USER_PROMPT_TEMPLATE.format(paper_text=paper_text)
    return SYSTEM_PROMPT, user_prompt


# ─── Metadata prompt ─────────────────────────────────────────

METADATA_SYSTEM_PROMPT = """你是一位学术论文分类专家。根据论文摘要，判断该论文的学科归属并提取关键词。

## 输出格式

返回严格的 JSON，格式如下：

```json
{
  "primary_discipline": "最主要的学科领域（英文，如 Information Retrieval）",
  "secondary_disciplines": ["次要学科1", "次要学科2"],
  "keywords": ["关键词1", "关键词2", "关键词3"]
}
```

字段说明：
- **primary_discipline**：该论文最核心的学科方向，单个字符串
- **secondary_disciplines**：涉及的其他学科方向，数组，可为空数组
- **keywords**：能代表论文核心内容的关键词，3-8个，英文"""

METADATA_USER_PROMPT_TEMPLATE = """请根据以下论文摘要，输出学科分类和关键词。

## 摘要

{abstract}

只输出 JSON，不要输出其他内容。"""


def build_metadata_prompt(abstract: str) -> tuple[str, str]:
    """构建 metadata 推断 prompt，返回 (system_prompt, user_prompt)。"""
    user_prompt = METADATA_USER_PROMPT_TEMPLATE.format(abstract=abstract)
    return METADATA_SYSTEM_PROMPT, user_prompt
