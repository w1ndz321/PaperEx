"""
gold_template.py — 金标准标注指南和模板

## 标注流程
1. 打开对应的 extracted JSON（kg_output/sciencedb_10_datasets_papers/<stem>.json）
2. 同时打开 MD 原文（markdown/sciencedb_10_datasets_papers/<stem>.md）
3. 逐条检查每个 extracted entry：
   - 类型是否正确？
   - 字段值是否准确？
   - evidence 是否忠实于原文？是否足够详细？
4. 补充 missing entries：LLM 漏抽的知识
5. 错误分类：
   - type_error: 类型判断错误（如 concept 被标为 method）
   - field_error: 字段值错误（如 quantity 名称不对）
   - evidence_short: evidence 缺乏关键上下文
   - evidence_mismatch: evidence 与知识声明不匹配
   - hallucination: 原文中不存在的内容
   - missing: 应该抽取但被遗漏的

## 金标准 JSON 格式
{
  "stem": "论文stem",
  "paper_title": "论文标题",
  "annotator": "标注者姓名",
  "annotated_at": "2026-05-11",
  "global_notes": "整体评价",
  "entries_eval": [
    {
      "entry_id": "doc_xxx_c1",       // 对应的 extracted entry id，缺失则 null
      "type": "concept",               // 知识类型
      "action": "correct" | "missing" | "remove",
      "issues": ["evidence_short"],    // 如有问题列出
      "correct_fields": {              // 正确的字段值（用于缺失条目或纠正）
        "term": "...",
        "normalized": "..."
      },
      "notes": "具体说明"
    }
  ],
  "type_stats": {
    "concept": {"extracted": 10, "correct": 8, "missing_gold": 3},
    ...
  }
}
"""

# 便捷函数
def create_gold_template(stem: str, title: str) -> dict:
    return {
        "stem": stem,
        "paper_title": title,
        "annotator": "",
        "annotated_at": "",
        "global_notes": "",
        "entries_eval": [],
        "type_stats": {},
    }
