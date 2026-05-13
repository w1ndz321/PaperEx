# 知识抽取系统评估框架

## 目录结构

```
eval/
  README.md              # 本文件
  selected_papers.txt    # 20 篇金标准标注论文列表
  gold_template.py       # 金标准标注模板和指南
  gold/                  # 金标准标注文件 (*.json)
  compute_coverage.py    # 知识覆盖率计算（召回率）
  compute_accuracy.py    # Evidence 准确率评估（LLM-as-Judge）
  ablation.py            # 结构化输出合法率消融实验
```

## 评估指标

### 1. 知识覆盖率 (Knowledge Coverage / Recall)
- **定义**: gold 中每条知识在 extracted 中被正确抽取的比例
- **计算**: 类型级匹配 (type + evidence_keywords + field_similarity)
- **输出**: 12 种类型的 recall + macro/micro average

### 2. Evidence 准确率 (Evidence Accuracy)
- **定义**: extracted entry 的 evidence 是否真正支撑其知识声明
- **计算**: LLM-as-Judge (evidence_match 1-5, completeness 1-5, hallucination)
- **输出**: per-type accuracy + 幻觉率

### 3. 结构化输出合法率 (Structural Validity)
- **定义**: LLM 输出能否被正确解析为符合 schema 的 JSON
- **消融**: Baseline vs +JSON修复 vs +Pydantic校验 vs Full

## 使用流程

### Step 1: 金标准标注
```bash
# 对每篇论文，创建 eval/gold/<stem>.json
# 格式参考 gold_template.py
```

### Step 2: 计算覆盖率
```bash
python eval/compute_coverage.py
```

### Step 3: 评估 Evidence 准确率
```bash
python eval/compute_accuracy.py  # 每篇抽样20条
```

### Step 4: 消融实验
```bash
python eval/ablation.py
```

## 初步消融实验结果

| 配置 | 合法率 | 提升 |
|------|--------|------|
| Baseline (无修复) | 40% | — |
| + JSON 截断修复 | **80%** | +40% |
| + Pydantic 校验 | 40% | 0 |
| Full (修复+校验) | **80%** | +40% |

> JSON 截断修复是提升结构化输出合法率的核心技术。
