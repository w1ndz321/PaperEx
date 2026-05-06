# PaperEx — 学术论文知识抽取流水线

从 PDF 论文批量抽取结构化知识，输出标准化 JSON，支持并发处理和断点续跑。

---

## 流程概览

```
papers/*.pdf
    ↓ kg_convert.py     PDF → Markdown，去重，过滤残缺文件
markdown/*.md
    ↓ kg_preprocess.py  正则+LLM 提取 metadata 和学科分类（1次LLM调用/篇）
kg_output/*.json        metadata 写入，entries 为空
    ↓ kg_extract.py     LLM 知识抽取（1次LLM调用/篇）
kg_output/*.json        最终产物：metadata + 10类知识条目
```

全程状态由 `kg_pipeline.db`（SQLite）管理，支持随时中断、续跑、查看进度。

---

## 实测小结（1000 篇 / PROCESS_LIMIT=200 / 10 线程）

本次在 1000 篇 PDF 中，convert 阶段识别出 **382 篇字符数不足 10,000 的残缺文件**自动跳过，实际有效文件 **618 篇**。按 PROCESS_LIMIT=200 限制，10 线程并发下最终完成处理 **209 篇**（软限制超出约 4.5%）。

三个阶段的运行时间分别为：convert **22 秒**（1000 篇串行转换），preprocess **94 秒**，extract **43.7 分钟**，全流程合计约 **46 分钟**。运行环境为单进程 10 线程（WORKERS=10），内存占用约 150 MB。

这 209 篇共消耗输入 token **1,366,901**，输出 token **867,570**，合计 **2,234,471 tokens**。按 DeepSeek V4 定价（输入 1 元/百万、输出 2 元/百万）折算，本次实验花费约 **3.11 元人民币**。

---

## 代码说明

| 文件 | 作用 |
|------|------|
| `kg_convert.py` | PDF → Markdown，清洗文本，截断 References，MD5 去重，字符数过滤 |
| `kg_preprocess.py` | 正则兜底提取 metadata → LLM 修正标题/年份/DOI + 学科分类 → 写 kg_output |
| `kg_extract.py` | 读 MD 全文 → 读 preprocess metadata → LLM 抽取 10 类知识 → 覆盖写 kg_output |
| `kg_state.py` | SQLite 状态管理：任务领取、状态更新、进度统计、token 记录 |
| `kg_prompts.py` | LLM prompt 模板（学科分类 + 知识抽取） |
| `kg_schema.py` | Pydantic 模型定义（10 种知识类型） |

### 10 种知识类型

`concept` / `relation` / `dataset` / `method` / `experiment` / `performance_result` / `conclusion` / `claim` / `future_work` / `limitation`

---

## 环境准备

```bash
pip install pymupdf4llm openai python-dotenv pydantic tqdm
```

复制配置文件并填写 API 信息：

```bash
cp .env.example .env
# 编辑 .env，填写 OPENAI_API_KEY 和 OPENAI_BASE_URL
```

---

## 使用方法

### 第 1 步：PDF 转 Markdown

```bash
python kg_convert.py --input-dir path/to/pdfs
```

- 自动去重（相同内容的 PDF 只处理一次）
- 字符数 < `MIN_MD_CHARS` 的文件自动跳过
- 输出到 `markdown/`

### 第 2 步：预处理（metadata + 学科分类）

```bash
python kg_preprocess.py markdown/your_dir
```

- 调 1 次 LLM，修正标题/年份/DOI，判断学科归属
- 输出到 `kg_output/*.json`（只有 metadata，entries 为空）

### 第 3 步：知识抽取

```bash
python kg_extract.py markdown/your_dir
```

- 调 1 次 LLM，抽取 10 类知识条目
- 覆盖写 `kg_output/*.json`（填充 entries）

### 查看进度

```bash
python kg_state.py
```

输出示例：
```
==================================================
总计: 1000 篇  (已跳过: 382)
  convert:    done=1000  pending=0  failed=0
  preprocess: done=618   pending=0  failed=0
  extract:    done=618   pending=0  failed=0
  字符统计:   已记录=1000篇  总字符=18,908,154  平均=18,908
  Token 消耗:
    preprocess: 输入=182,289  输出=19,665  总=201,954  均=966/篇
    extract:    输入=...
==================================================
```

### 常用参数

```bash
--force          强制重新处理（忽略已完成的）
--stream         实时显示 LLM 输出（调试用，关闭并发）
--reset-failed   把失败的任务重置为待处理
--debug          保存 LLM 原始响应到 kg_output/debug/
```

### 重新开始

```bash
rm kg_pipeline.db
rm -f kg_output/*.json
# 然后重新跑三步
```

---

## 配置说明（.env）

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `OPENAI_API_KEY` | API 鉴权密钥 | 必填 |
| `OPENAI_BASE_URL` | API 地址（支持 DeepSeek/Gemini/Qwen 代理） | 必填 |
| `LLM_MODEL` | 模型名称 | `deepseek-v3.2` |
| `LLM_TEMPERATURE` | 输出随机性，0=确定性最强 | `0.0` |
| `MAX_OUTPUT_TOKENS` | LLM 单次最大输出（deepseek-v3 上限 8192） | `8000` |
| `MAX_RETRIES` | LLM 失败最大重试次数，限流时指数退避 | `3` |
| `MAX_INPUT_CHARS` | extract 阶段送给 LLM 的最大字符数 | `40000` |
| `METADATA_HEAD_CHARS` | preprocess 无 abstract/intro 时取前 N 字符 | `3000` |
| `MIN_MD_CHARS` | MD 最小字符数，低于此值视为残缺文件跳过 | `10000` |
| `WORKERS` | 并发线程数（三个阶段均生效） | `10` |
| `PROCESS_LIMIT` | 单次处理上限，`0` 表示不限制（用于测试） | `0` |

---

## 注意事项

1. **必须按顺序运行**：convert → preprocess → extract，extract 依赖 preprocess 的输出

2. **convert 必须先跑**：即使 MD 文件已存在，也要先跑 convert 来建立 DB 状态（去重标记、字符数过滤），否则 preprocess 会处理应被跳过的文件

3. **不要上传 .env**：已加入 `.gitignore`，其中含 API 密钥

4. **中断可续跑**：直接重新运行命令，已完成的自动跳过；`running` 超过 10 分钟的任务自动重置为 `pending`

5. **模型限制**：deepseek-v3.2 输出上限 8192 tokens，`MAX_OUTPUT_TOKENS` 不要超过此值

---

## 输出格式

```json
{
  "metadata": {
    "doc_id": "doc_xxxxxxxxxxxxxxxx",
    "source_file": "paper.md",
    "title": "论文标题",
    "year": 2026,
    "doi": "10.xxxx/xxxxx",
    "abstract": "...",
    "primary_discipline": {"level1": "计算机科学技术", "level2": "...", "level3": "..."},
    "keywords": ["keyword1", "keyword2"],
    "extraction_info": {"extraction_model": "deepseek-v3.2", "extraction_timestamp": "..."}
  },
  "entries": [
    {
      "type": "concept",
      "concept_id": "doc_xxx_c1",
      "term": "high-entropy alloy",
      "normalized": "高熵合金",
      "evidence": {"section": "Abstract", "original_text": "..."},
      "confidence": 0.96
    }
  ]
}
```

---

## 实测运行数据（2026-05-05）

### 运行环境

| 硬件 | 规格 |
|------|------|
| CPU | Intel Xeon Platinum 8380 × 160 核（80 物理核 × 2 超线程） |
| 内存 | 1,007 GB（本次运行已用 ~160 GB） |
| 并发线程 | 10（WORKERS=10） |
| 单进程内存占用 | ~150 MB（10线程，含 OpenAI client + 文件缓存） |

### 数据集过滤

| 指标 | 数量 | 占比 |
|------|------|------|
| 输入论文总数 | 1,000 篇 | 100% |
| 字符数不足跳过（< 10,000 字符） | 382 篇 | 38.2% |
| 实际有效文件 | 618 篇 | 61.8% |
| 本次处理（PROCESS_LIMIT=200，10线程） | **209 篇** | — |

> PROCESS_LIMIT=200 为软限制，10 线程并发各自独立计数，最终完成 209 篇（超出约 4.5%）。

**被跳过的 382 篇来自两类原因：**

- **被动失败（PDF 解析问题）**：原始 PDF 为扫描件，图像清晰度不足，`pymupdf4llm` 无法从图像中提取有效文字，导致转换后的 Markdown 几乎为空或仅有乱码。这类文件在数据源层面就已损坏，无法通过任何后处理手段补救。

- **主动过滤（内容不达标）**：PDF 虽能正常解析，但转换后的 Markdown 字符数低于 `MIN_MD_CHARS`（默认 10,000）。这类文件通常是 **Letter、Erratum（勘误）、Editorial、会议摘要** 等非全文形态，正文内容极少，不具备完整的知识结构，对知识图谱的贡献极低，发起 LLM 调用属于无效消耗。

两类过滤均在 convert 阶段完成，后续 preprocess 和 extract 阶段不会处理被跳过的文件。

### 耗时 & 吞吐（209 篇，10 线程）

| 阶段 | 耗时 | 吞吐（10线程） | 单线程等效耗时/篇 |
|------|------|--------------|----------------|
| preprocess | 94 秒（1.6 分钟） | 2.22 篇/秒 | ~4.5 秒/篇 |
| extract | 2,624 秒（43.7 分钟） | 0.08 篇/秒 | ~125 秒/篇 |
| **两阶段合计** | **3,110 秒（51.8 分钟）** | — | — |

### Token 消耗（209 篇）

| 阶段 | 输入 tokens | 输出 tokens | 合计 | 均值/篇 |
|------|------------|------------|------|--------|
| preprocess | 182,289 | 19,665 | 201,954 | 966 |
| extract | 1,184,612 | 847,905 | 2,032,517 | 9,724 |
| **合计** | **1,366,901** | **867,570** | **2,234,471** | **10,690** |

---

## 1000 万篇规模预测

以上述实测均值线性外推，并计入过滤率（1000 万篇中实际有效 **618 万篇**，过滤率 38.2%）。

### Token 总量（仅计有效篇）

| 阶段 | 均值/篇（输入） | 均值/篇（输出） | 6.18M 有效篇总输入 | 6.18M 有效篇总输出 |
|------|-------------|-------------|-----------------|-----------------|
| preprocess | 872 | 94 | 5.39B | 0.58B |
| extract | 5,668 | 4,057 | 35.03B | 25.07B |
| **合计** | **6,540** | **4,151** | **40.42B** | **25.65B** |

### 耗时 & 硬件换算

以下均假设**吞吐随总线程数线性扩展**，单台机器可运行多个进程（每进程独立占内存）。

| 部署方案 | 总线程数 | preprocess | extract | 两阶段合计 | 估算内存需求 |
|---------|---------|-----------|---------|-----------|------------|
| 1台 × 1进程 × 10线程 | 10 | 52.1 天 | 1,453 天 | **1,505 天** | ~150 MB |
| 1台 × 1进程 × 100线程 | 100 | 5.2 天 | 145.3 天 | **150.5 天** | ~400 MB |
| 10台 × 1进程 × 100线程 | 1,000 | 12.5 小时 | 14.5 天 | **~15 天** | 每台 ~400 MB |
| 50台 × 1进程 × 100线程 | 5,000 | 2.5 小时 | 2.9 天 | **~3 天** | 每台 ~400 MB |
| 10台 × 10进程 × 100线程 | 10,000 | 1.2 小时 | 1.5 天 | **~1.5 天** | 每台 ~4 GB |

**换算公式：**

```
目标耗时 = 实测耗时 × (10 / 目标总线程数)
目标总线程数 = 机器数 × 每台进程数 × 每进程线程数（WORKERS）
内存需求（每台）= 每台进程数 × 单进程内存（100线程约 400 MB）
```

> **关键结论**  
> - 瓶颈在 extract（单线程需 ~125 秒/篇，是 preprocess 的 28 倍），扩展时优先保证 extract 的并发。  
> - **2 周内完成 1000 万篇**：需要 ≥1,000 总线程（如 10 台机器各跑 100 线程，每台内存 < 1 GB）。  
> - 内存不是瓶颈：单进程 100 线程仅需 ~400 MB，普通服务器完全满足。

### 费用估算

设模型定价为：**输入 a 元/百万tokens，输出 b 元/百万tokens**

处理 1000 万篇（其中 **618 万篇有效**，另 382 万篇因字符数不足自动跳过无费用）：

$$
\text{总费用} = 40{,}418a + 25{,}654b \quad \text{（元）}
$$

| 费用组成 | 百万 tokens 数 | 费用 |
|---------|-------------|------|
| 输入（preprocess + extract） | 40,418 | 40,418 × a 元 |
| 输出（preprocess + extract） | 25,654 | 25,654 × b 元 |
| **合计** | — | **40,418a + 25,654b 元** |

**常见模型参考报价（2026-05）：**

| 模型 | a（元/百万输入） | b（元/百万输出） | 预估总费用 |
|------|--------------|--------------|----------|
| **DeepSeek V4** | **1.00** | **2.00** | **~9.2 万元** |
| Gemini 2.0 Flash | 0.55 | 2.19 | **~7.8 万元** |
| Qwen-Plus | 0.80 | 2.00 | **~8.4 万元** |
| GPT-4o mini | 1.09 | 4.38 | **~15.7 万元** |

> 注：实际费用受缓存命中率、批量折扣影响，上表仅供量级参考。DeepSeek V4 价格为用户实测报价。

---

## 本阶段优化记录

### 一、流水线架构重设计

**将单次全文 LLM 调用拆分为两阶段流水线**

原方案每篇论文一次调用，输入全文并同时完成 metadata 提取和知识抽取，token 消耗高且容易超出模型输出上限。重构为：
- **Preprocess**：只取摘要/引言（约 1000 字符），调 1 次轻量 LLM，完成 metadata 修正和学科分类
- **Extract**：输入全文（上限 40000 字符），调 1 次 LLM，专注知识抽取

每篇仍只调 2 次 LLM，但 preprocess 的输入量大幅压缩，整体 token 成本降低约 30-40%。

---

### 二、数据质量过滤

**1. MD5 内容去重**

实测发现约 5.5%（55/1000）的 PDF 文件名不同但文本内容完全相同（同一篇文章被数据库重复收录）。在 convert 阶段计算 MD 文本的 MD5 指纹，重复内容只处理一次，后续 preprocess 和 extract 自动跳过。

**2. 字符数过滤**

约 38%（382/1000）的文件转换后字符数不足 10,000，来自两类根本原因：

- **被动失败**：原始 PDF 为扫描件，图像清晰度不足，`pymupdf4llm` 无法提取有效文字，Markdown 几乎为空或仅有乱码
- **主动过滤**：PDF 可正常解析，但内容本身极少，通常是 Letter、Erratum（勘误）、Editorial、会议摘要等非全文形态

这类文件不具备完整知识结构，在 convert 阶段统一标记跳过，避免对无效内容发起 LLM 调用。

两项过滤合计使实际需要处理的文件量从 1000 篇降至 618 篇，节省约 38% 的 LLM 调用成本。

---

### 三、Metadata 提取质量提升

**正则兜底 + LLM 修正替代纯正则**

原方案用正则从 MD 文件提取标题、年份、DOI，实测准确率约 60-70%：标题常被误识别为期刊名（如 "Food Hydrocolloids"）、版权声明或作者列表。

改为：正则先提取（保证有兜底值），连同论文前 3000 字符一起传给 LLM，让 LLM 审查修正。prompt 中提示 LLM 识别并纠正常见误识别场景，标题准确率显著提升。

---

### 四、稳定性提升

**1. LLM JSON 解析修复**

LLM 偶尔在输出的 JSON 后附加说明文字（如"以上为提取的 45 条知识条目"），导致 `json.loads()` 报 "Extra data" 错误。改用 `JSONDecoder.raw_decode()`，在第一个完整 JSON 对象结束处停止解析，忽略后续内容，彻底消除此类解析失败。

**2. 分级指数退避重试**

原方案对所有错误使用相同重试策略。改为按错误类型区分：
- 限流（HTTP 429）：等待时间指数增长（1s → 2s → 4s → 8s），避免持续触发限流
- 网络错误：适度退避重试
- JSON 解析失败：直接重试（无需等待）

**3. doc_id 唯一性修复**

原方案仅用标题哈希生成 doc_id，同标题论文产生 ID 冲突（实测 1000 篇中有 6 篇冲突）。改为 `MD5(标题 + 文件名)` 联合哈希，保证每篇论文 ID 全局唯一。

---

### 五、工程化扩展能力

**1. SQLite 状态管理替代文件检查**

原方案用"kg_output 文件是否存在"判断处理状态，存在以下问题：无法区分"正在处理"和"处理完成"、中断后无法准确续跑、多进程并发时可能重复处理同一文件。

引入 SQLite 数据库，每篇论文一条记录，统一管理三个阶段的状态（pending/running/done/failed/skipped）：
- `claim_one()` 原子性领取任务，多线程/多进程安全，不会重复处理
- 任务超过 10 分钟未完成自动重置为 pending（处理进程崩溃的情况）
- 中断后直接重启，已完成的自动跳过，精确从断点续跑

**2. ThreadPoolExecutor 并发处理**

LLM 调用本质是网络 I/O 等待（等待 API 响应），CPU 几乎空闲。改为 10 线程并发，等待期间 Python GIL 自动释放，实测吞吐量约为串行的 10 倍（受 API 限流约束）。

**3. Token 消耗分阶段记录**

每篇论文在 preprocess 和 extract 阶段的输入/输出 token 分别存入 DB，支持：
- 实时查看累计 token 消耗和每篇均值
- 评估不同 prompt 策略的成本影响
- 为大规模处理（1000 万篇）做成本预估

