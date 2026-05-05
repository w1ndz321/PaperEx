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
