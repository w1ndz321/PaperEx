# 知识抽取系统 Schema

## 一、Metadata 结构

每篇论文抽取结果包含一个 `metadata` 对象。

| 字段 | 必填 | 说明 |
|------|------|------|
| `title` | 是 | 论文标题 |
| `year` | 否 | 发表年份 |
| `doi` | 否 | DOI 编号 |
| `doc_id` | 是 | 文档唯一标识，MD5(title\|stem) |
| `source_file` | 是 | 原始 MD 文件名 |
| `abstract` | 否 | 摘要 |
| `introduction` | 否 | 引言内容 |
| `primary_discipline` | 是 | 主学科 level1/level2/level3 |
| `secondary_disciplines` | 否 | 辅助学科数组 |
| `keywords` | 是 | 关键词列表 |
| `extraction_info.extraction_model` | 是 | LLM 模型名称 |
| `extraction_info.extraction_method` | 是 | 抽取方法（grouped_serial_5groups） |
| `extraction_info.extraction_timestamp` | 是 | ISO 8601 时间戳 |
| `extraction_info.failed_groups` | 否 | 失败组列表（增量重试） |

**抽取流程**：convert(PDF→MD) → preprocess(metadata+学科,1次LLM) → extract(5组串行LLM)

---

## 二、知识类型定义

共 12 种知识类型，5 组串行抽取。每条知识包含 `type`、类型 ID、`evidence`（8-10句原文摘录）、`confidence`。

### G1: concept + relation（概念层）

#### concept

| 字段 | 必填 | 说明 |
|------|------|------|
| `concept_id` | 是 | doc_xxx_cN |
| `term` | 是 | 原文术语 |
| `normalized` | 是 | 规范化中文名 |
| `std_label` | 否 | 标准缩写 |

#### relation

| 字段 | 必填 | 说明 |
|------|------|------|
| `relation_id` | 是 | doc_xxx_rN |
| `head` | 是 | 起始概念 concept_id |
| `head_term` | 是 | 起始概念原文 term |
| `relation_type` | 是 | enhances/inhibits/causes/belongs_to/measures/uses/compares/precedes/derives |
| `relation_surface` | 是 | 原文关系动词 |
| `tail` | 是 | 目标概念 concept_id |
| `tail_term` | 是 | 目标概念原文 term |

---

### G2: dataset + data_specification（数据资源层）

#### dataset

| 字段 | 必填 | 说明 |
|------|------|------|
| `dataset_id` | 是 | doc_xxx_dN |
| `name` | 是 | 数据集名称 |
| `modality` | 否 | text / image / tabular / time_series / multimodal / other |
| `domain` | 否 | 所属领域 |

#### data_specification

| 字段 | 必填 | 说明 |
|------|------|------|
| `ds_id` | 是 | doc_xxx_dsN |
| `spec_type` | 是 | format_rule / quality_standard / env_requirement / metadata_standard |
| `description` | 否 | 一句话摘要 |

---

### G3: method + experiment（方法实验层）

#### method

| 字段 | 必填 | 说明 |
|------|------|------|
| `method_id` | 是 | doc_xxx_mN |
| `name` | 是 | 方法/模型/仪器名称 |
| `method_type` | 是 | model / algorithm / protocol / software / instrument / preprocessing |

#### experiment

| 字段 | 必填 | 说明 |
|------|------|------|
| `experiment_id` | 是 | doc_xxx_xN |
| `task` | 是 | 实验任务名称 |
| `setup` | 否 | 实验条件摘要 |

---

### G4: quantitative_result + performance_result（结果指标层）

#### quantitative_result（科学度量与实验指标，排除年份/页数/编号等元信息）

| 字段 | 必填 | 说明 |
|------|------|------|
| `qr_id` | 是 | doc_xxx_qrN |
| `quantity` | 是 | 物理量/指标名称 |
| `value` | 否 | 数值 |
| `unit` | 否 | 单位 |
| `context` | 是 | 实验条件/上下文 |
| `result_type` | 是 | main_result / baseline / ablation / measurement / threshold |

#### performance_result

| 字段 | 必填 | 说明 |
|------|------|------|
| `perf_id` | 是 | doc_xxx_pN |
| `metric` | 否 | 被比较的指标名称 |
| `compared_to` | 否 | 对比对象 |

---

### G5: claim + conclusion + limitation + future_work（结论展望层）

四类均仅需 evidence 字段，无额外标注字段。

| 类型 | ID 字段 | 说明 |
|------|--------|------|
| `claim` | `claim_id` | 核心主张/发现 |
| `conclusion` | `conclusion_id` | 经实验验证的结论 |
| `limitation` | `limitation_id` | 方法局限、适用约束 |
| `future_work` | `future_work_id` | 未来研究方向 |

---

## 三、抽取原则

1. **忠实性**：`original_text` 必须是原文直接摘录，禁止改写
2. **完整性**：每条 evidence 8-10 句完整段落，保留实验条件、数值、对比基准等全部细节
3. **关联性**：relation 的 head/tail 必须对应已抽取的 concept
4. **不设数量配额**：原文有的全抽，不编造；组内各类型均衡分配
5. **quality over quantity**：quantitative_result 必须排除年份、页数、编号等元信息
