# 知识抽取系统 Schema

## 一、Metadata 结构

每篇论文抽取结果包含一个 `metadata` 对象，记录论文基本信息。

```json
{
  "metadata": {
    "title": "High-entropy alloy enables multi-path electron synergism for enhanced oxygen evolution activity",
    "year": 2025,
    "doi": "10.1038/s41467-025-58648-y",
    "doc_id": "doc_3058031503d94b2c",
    "abstract": "Electrocatalytic oxygen evolution reaction (OER) is key to several energy technologies but suffers from low activity...",
    "introduction": "We analyzed the catalyst surface using Raman spectroscopy...",
    "primary_discipline": {
      "level1": "化学",
      "level2": "物理化学",
      "level3": "电化学"
    },
    "secondary_disciplines": [
      {
        "level1": "材料科学",
        "level2": "金属材料",
        "level3": "合金材料"
      }
    ],
    "keywords": ["高熵合金", "电催化", "氧析出反应", "晶格氧活化机制"],
    "extraction_info": {
      "extraction_model": "gemini-2.5-pro",
      "extraction_timestamp": "2026-04-02T10:00:00+08:00"
    }
  }
}
```

**字段说明**：

| 字段 | 必填 | 说明 |
|------|------|------|
| `title` | 是 | 论文标题，从 markdown 解析 |
| `year` | 是 | 发表年份，从 Published/Date 等关键词解析 |
| `doi` | 否 | DOI，从原文解析 |
| `doc_id` | 是 | 文档唯一标识，根据 title 生成 MD5 |
| `abstract` | 是 | 摘要，从 markdown 解析 |
| `introduction` | 是 | 引言章节内容 |
| `primary_discipline` | 是 | 主学科，包含 level1/level2/level3 |
| `secondary_disciplines` | 否 | 辅助学科数组，可为 `null` |
| `keywords` | 是 | 关键词列表，优先从原文提取，无则由 LLM 推断 |
| `extraction_info.extraction_model` | 是 | 使用的 LLM 模型名称 |
| `extraction_info.extraction_timestamp` | 是 | 抽取时间，ISO 8601 格式 |

**学科分类说明**：
- `primary_discipline` 和 `secondary_disciplines` 根据 `disciplines.json` 中定义的学科目录分类
- **输入**：abstract + introduction
- 学科名称必须严格匹配 `disciplines.json` 中的定义
- 如果某级学科无法确定，对应字段可为 `null`

---

## 二、知识类型定义

共 10 种知识类型，采用"原文段落 + 轻标注"模式。

### 1. concept（概念）

论文中定义或使用的关键概念、术语、实体。

```json
{
  "type": "concept",
  "concept_id": "doc_<doc_id>_c<local_id>",
  "term": "Oxygen evolution reaction",
  "normalized": "氧析出反应",
  "std_label": "OER",
  "evidence": {
    "section": "Abstract",
    "original_text": "Electrocatalytic oxygen evolution reaction (OER) is key to several energy technologies but suffers from low activity."
  },
  "confidence": 0.95
}
```

**字段说明**：
| 字段 | 必填 | 说明 |
|------|------|------|
| `term` | 是 | 原文中的术语，保持原文大小写 |
| `normalized` | 是 | 中文翻译/标准化名称 |
| `std_label` | 否 | 缩写（如有），如 OER、RAG |
| `evidence.section` | 是 | 章节名称 |
| `evidence.original_text` | 是 | 原文片段，3-6 句，保留上下文 |
| `confidence` | 是 | 信心程度，0.0-1.0 |

---

### 2. relation（关系）

概念之间的语义关系。

```json
{
  "type": "relation",
  "relation_id": "doc_<doc_id>_r<local_id>",
  "head": "doc_<doc_id>_c1",
  "head_term": "high-entropy alloy",
  "relation_type": "enhances",
  "relation_surface": "can efficiently activate",
  "tail": "doc_<doc_id>_c2",
  "tail_term": "oxygen evolution reaction",
  "evidence": {
    "section": "Abstract",
    "original_text": "We reveal that high-entropy alloys (HEAs) can efficiently activate the LOM through synergistic multi-path electron transfer..."
  },
  "confidence": 0.93
}
```

**字段说明**：
| 字段 | 必填 | 说明 |
|------|------|------|
| `head` | 是 | 起始概念的 concept_id |
| `head_term` | 是 | 起始概念的 term（便于阅读） |
| `relation_type` | 是 | 关系类型，由 LLM 自由生成 |
| `relation_surface` | 是 | 原文中表达该关系的具体词汇 |
| `tail` | 是 | 目标概念的 concept_id |
| `tail_term` | 是 | 目标概念的 term（便于阅读） |
| `evidence.section` | 是 | 章节名称 |
| `evidence.original_text` | 是 | 原文片段，3-6 句，保留上下文 |
| `confidence` | 是 | 信心程度，0.0-1.0 |

---

### 3. dataset（数据集与基准）

论文中提及或使用的数据集和基准。

```json
{
  "type": "dataset",
  "dataset_id": "doc_<doc_id>_d<local_id>",
  "name": "FreeSolv",
  "samples": 642,
  "domain": "chemistry",
  "evidence": {
    "section": "Section 2",
    "original_text": "We evaluate our model on the FreeSolv dataset, which contains 642 small molecules with experimental solvation free energies..."
  },
  "confidence": 0.93
}
```

**字段说明**：
| 字段 | 必填 | 说明 |
|------|------|------|
| `name` | 是 | 数据集名称 |
| `samples` | 否 | 样本数量 |
| `domain` | 否 | 领域（chemistry, biology, NLP, CV...） |
| `evidence.section` | 是 | 章节名称 |
| `evidence.original_text` | 是 | 原文片段，3-6 句，保留上下文 |
| `confidence` | 是 | 信心程度，0.0-1.0 |

---

### 4. method（方法）

论文使用或提出的方法、模型、算法、仪器。

```json
{
  "type": "method",
  "method_id": "doc_<doc_id>_m<local_id>",
  "name": "D-MPNN",
  "method_type": "model",
  "evidence": {
    "section": "Methods",
    "original_text": "We employ D-MPNN (Directed Message Passing Neural Network) for molecular property prediction. The model takes molecular graphs as input and learns representations through message passing along directed edges."
  },
  "confidence": 0.95
}
```

**字段说明**：
| 字段 | 必填 | 说明 |
|------|------|------|
| `name` | 是 | 方法/模型/仪器名称 |
| `method_type` | 是 | `model` / `algorithm` / `protocol` / `software` / `instrument` / `preprocessing` |
| `evidence.section` | 是 | 章节名称 |
| `evidence.original_text` | 是 | 原文片段，3-6 句，保留上下文 |
| `confidence` | 是 | 信心程度，0.0-1.0 |

---

### 5. experiment（实验）

实验设置、流程及关键参数，包含物理量约束和实验条件。

```json
{
  "type": "experiment",
  "experiment_id": "doc_<doc_id>_x<local_id>",
  "task": "electrochemical stability test",
  "evidence": {
    "section": "Methods",
    "original_text": "All electrochemical measurements were performed at 298 K under ambient pressure using a standard three-electrode configuration. The current density was maintained at 10 mA/cm² during the stability test in 1M KOH solution."
  },
  "confidence": 0.93
}
```

**字段说明**：
| 字段 | 必填 | 说明 |
|------|------|------|
| `task` | 是 | 原文中实验任务的名称或描述，直接摘自原文，不总结 |
| `evidence.section` | 是 | 章节名称 |
| `evidence.original_text` | 是 | 原文片段，3-6 句，保留上下文 |
| `confidence` | 是 | 信心程度，0.0-1.0 |

---

### 6. performance_result（性能结果）

模型/方法在评估任务上的性能指标。

```json
{
  "type": "performance_result",
  "perf_id": "doc_<doc_id>_p<local_id>",
  "evidence": {
    "section": "Table 2",
    "original_text": "Our model achieves an RMSE of 1.15 kcal/mol on the FreeSolv benchmark with scaffold split, outperforming previous baselines including MPNN (1.34 kcal/mol) and SchNet (1.22 kcal/mol)."
  },
  "confidence": 0.93
}
```

**字段说明**：
| 字段 | 必填 | 说明 |
|------|------|------|
| `evidence.section` | 是 | 章节名称 |
| `evidence.original_text` | 是 | 原文片段，3-6 句，包含指标名称、数值、单位、对比信息 |
| `confidence` | 是 | 信心程度，0.0-1.0 |

---

### 7. conclusion（结论）

论文的核心结论，通常来自 Conclusion 或 Discussion 章节。

```json
{
  "type": "conclusion",
  "conclusion_id": "doc_<doc_id>_cl<local_id>",
  "evidence": {
    "section": "Conclusion",
    "original_text": "Our results demonstrate that high-entropy alloys enable multi-path electron transfer to synergistically activate the lattice oxygen mechanism, providing a new design strategy for efficient OER catalysts."
  },
  "confidence": 0.95
}
```

**字段说明**：
| 字段 | 必填 | 说明 |
|------|------|------|
| `evidence.section` | 是 | 章节名称 |
| `evidence.original_text` | 是 | 原文片段，3-6 句，保留上下文 |
| `confidence` | 是 | 信心程度，0.0-1.0 |

---

### 8. claim（核心声明）

论文提出的核心主张、发现或假设，通常是作者认为最重要的贡献陈述。

```json
{
  "type": "claim",
  "claim_id": "doc_<doc_id>_ca<local_id>",
  "evidence": {
    "section": "Abstract",
    "original_text": "Here we report that configurational entropy in high-entropy alloys synergistically activates multiple electron transfer pathways, fundamentally different from conventional single-element active site optimization, enabling superior OER performance."
  },
  "confidence": 0.95
}
```

**字段说明**：
| 字段 | 必填 | 说明 |
|------|------|------|
| `evidence.section` | 是 | 章节名称 |
| `evidence.original_text` | 是 | 原文片段，3-6 句，包含作者的核心主张 |
| `confidence` | 是 | 信心程度，0.0-1.0 |

---

### 9. future_work（未来工作）

论文明确提出的下一步研究方向或待解决问题。

```json
{
  "type": "future_work",
  "future_work_id": "doc_<doc_id>_fw<local_id>",
  "evidence": {
    "section": "Discussion",
    "original_text": "Future studies should explore the application of high-entropy alloys to other electrocatalytic reactions such as CO2 reduction and nitrogen reduction, and investigate the role of entropy at elevated temperatures."
  },
  "confidence": 0.93
}
```

**字段说明**：
| 字段 | 必填 | 说明 |
|------|------|------|
| `evidence.section` | 是 | 章节名称 |
| `evidence.original_text` | 是 | 原文片段，3-6 句，保留上下文 |
| `confidence` | 是 | 信心程度，0.0-1.0 |

---

### 10. limitation（局限性）

论文明确指出的方法局限、适用范围约束或已知不足。

```json
{
  "type": "limitation",
  "limitation_id": "doc_<doc_id>_lm<local_id>",
  "evidence": {
    "section": "Discussion",
    "original_text": "Our approach currently struggles with molecules containing more than 50 heavy atoms, which we identify as a key limitation for future work. The message passing mechanism becomes computationally expensive for large molecules."
  },
  "confidence": 0.93
}
```

**字段说明**：
| 字段 | 必填 | 说明 |
|------|------|------|
| `evidence.section` | 是 | 章节名称 |
| `evidence.original_text` | 是 | 原文片段，3-6 句，保留上下文 |
| `confidence` | 是 | 信心程度，0.0-1.0 |

---

## 三、完整示例

```json
{
  "metadata": {
    "title": "High-entropy alloy enables multi-path electron synergism for enhanced oxygen evolution activity",
    "year": 2025,
    "doi": "10.1038/s41467-025-58648-y",
    "doc_id": "doc_3058031503d94b2c",
    "abstract": "Electrocatalytic oxygen evolution reaction (OER) is key to several energy technologies but suffers from low activity...",
    "introduction": "We analyzed the catalyst surface using Raman spectroscopy...",
    "primary_discipline": {
      "level1": "化学",
      "level2": "物理化学",
      "level3": "电化学"
    },
    "secondary_disciplines": null,
    "keywords": ["high-entropy alloy", "electrocatalysis", "oxygen evolution", "lattice oxygen mechanism"],
    "extraction_info": {
      "extraction_model": "gpt-5.4",
      "extraction_timestamp": "2026-04-17T10:00:00+08:00"
    }
  },
  "entries": [
    {
      "type": "concept",
      "concept_id": "doc_3058031503d94b2c_c1",
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
      "type": "concept",
      "concept_id": "doc_3058031503d94b2c_c2",
      "term": "oxygen evolution reaction",
      "normalized": "氧析出反应",
      "std_label": "OER",
      "evidence": {
        "section": "Abstract",
        "original_text": "Electrocatalytic oxygen evolution reaction (OER) is key to several energy technologies but suffers from low activity. Here we report that high-entropy alloys can efficiently activate the lattice oxygen mechanism for enhanced OER performance."
      },
      "confidence": 0.98
    },
    {
      "type": "relation",
      "relation_id": "doc_3058031503d94b2c_r1",
      "head": "doc_3058031503d94b2c_c1",
      "head_term": "high-entropy alloy",
      "relation_type": "enhances",
      "relation_surface": "can efficiently activate",
      "tail": "doc_3058031503d94b2c_c2",
      "tail_term": "oxygen evolution reaction",
      "evidence": {
        "section": "Abstract",
        "original_text": "We reveal that high-entropy alloys (HEAs) can efficiently activate the LOM through synergistic multi-path electron transfer for enhanced oxygen evolution activity."
      },
      "confidence": 0.93
    },
    {
      "type": "dataset",
      "dataset_id": "doc_3058031503d94b2c_d1",
      "name": "OER activity benchmark",
      "samples": null,
      "domain": "electrochemistry",
      "evidence": {
        "section": "Results",
        "original_text": "We benchmark our FeCoNiCrMn HEA against state-of-the-art OER catalysts including IrO2 and RuO2, evaluating overpotential at 10 mA/cm² and Tafel slope in 1M KOH solution."
      },
      "confidence": 0.90
    },
    {
      "type": "method",
      "method_id": "doc_3058031503d94b2c_m1",
      "name": "Raman spectroscopy",
      "method_type": "instrument",
      "evidence": {
        "section": "Methods",
        "original_text": "We analyzed the catalyst surface using Raman spectroscopy following the i-t tests in both KOH and TMAOH solutions. In situ Raman spectra were collected using a 532 nm laser at a power of 5 mW."
      },
      "confidence": 0.95
    },
    {
      "type": "experiment",
      "experiment_id": "doc_3058031503d94b2c_x1",
      "task": "electrochemical stability test",
      "evidence": {
        "section": "Methods",
        "original_text": "All electrochemical measurements were performed at 298 K under ambient pressure using a standard three-electrode configuration. The current density was maintained at 10 mA/cm² during the 100-hour stability test in 1M KOH solution."
      },
      "confidence": 0.95
    },
    {
      "type": "performance_result",
      "perf_id": "doc_3058031503d94b2c_p1",
      "evidence": {
        "section": "Results",
        "original_text": "The FeCoNiCrMn HEA exhibits a low overpotential of 280 mV at a current density of 10 mA/cm² in 1M KOH solution, along with a small Tafel slope of 42 mV/dec, outperforming IrO2 (320 mV) and RuO2 (310 mV)."
      },
      "confidence": 0.95
    },
    {
      "type": "claim",
      "claim_id": "doc_3058031503d94b2c_ca1",
      "evidence": {
        "section": "Abstract",
        "original_text": "Here we report that configurational entropy in high-entropy alloys synergistically activates multiple electron transfer pathways, fundamentally different from conventional single-element active site optimization, enabling superior OER performance."
      },
      "confidence": 0.96
    },
    {
      "type": "conclusion",
      "conclusion_id": "doc_3058031503d94b2c_cl1",
      "evidence": {
        "section": "Conclusion",
        "original_text": "Our results demonstrate that high-entropy alloys enable multi-path electron transfer to synergistically activate the lattice oxygen mechanism, providing a new design strategy for efficient OER catalysts beyond conventional single-element active site optimization."
      },
      "confidence": 0.96
    },
    {
      "type": "limitation",
      "limitation_id": "doc_3058031503d94b2c_lm1",
      "evidence": {
        "section": "Discussion",
        "original_text": "The current study is limited to five-component HEAs in alkaline media; the generalizability to acid-stable compositions and other electrolytes remains to be demonstrated in future work."
      },
      "confidence": 0.92
    },
    {
      "type": "future_work",
      "future_work_id": "doc_3058031503d94b2c_fw1",
      "evidence": {
        "section": "Discussion",
        "original_text": "Future studies should explore the application of high-entropy alloys to other electrocatalytic reactions such as CO2 reduction and nitrogen reduction, and investigate the compositional space beyond five-component systems."
      },
      "confidence": 0.93
    }
  ]
}
```

---

## 四、抽取原则

1. **忠实性**：`original_text` 必须是原文的直接摘录，禁止改写或编造
2. **完整性**：`original_text` 包含 3-6 个完整句子，保留充分上下文
3. **关联性**：relation 的 head/tail 必须对应已抽取的 concept
4. **轻标注**：字段值简短，用短语而非完整句子
5. **覆盖度**：每篇论文 20-50 条记录，覆盖尽可能多的类型；claim/conclusion/limitation/future_work 不是每篇论文都有，按实际内容抽取
