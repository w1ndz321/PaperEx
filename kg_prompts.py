"""
kg_prompts.py — 论文知识抽取的 prompt 模板

学科分类 prompt: 传入 abstract+intro（或前N字符），LLM 输出 title/year/doi + 学科 + keywords
知识抽取 prompt: 传入论文全文，LLM 输出 12 类知识条目
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
         "std_label": "HEA",
         "evidence": {"section": "Abstract", "original_text": "We reveal that high-entropy alloys (HEAs) can efficiently activate the LOM through synergistic multi-path electron transfer. Configurational entropy in these multi-principal-element alloys stabilizes a single-phase solid solution, enabling unique catalytic properties not achievable in binary or ternary systems. Unlike conventional alloys that rely on one or two principal elements, HEAs contain five or more principal elements in near-equimolar ratios, creating a vast compositional space. The high configurational entropy lowers the Gibbs free energy, stabilizing disordered solid solution phases over intermetallic compounds. This entropic stabilization has been exploited in various fields including structural materials, catalysis, and energy storage. The resulting homogeneous elemental distribution at the atomic scale gives rise to unique electronic structures that are fundamentally different from those of dilute alloys."},
         "confidence": 0.96},
        {"type": "concept", "concept_id": "doc_xxx_c2", "term": "oxygen evolution reaction", "normalized": "氧析出反应",
         "std_label": "OER",
         "evidence": {"section": "Abstract", "original_text": "Electrocatalytic oxygen evolution reaction (OER) is key to several energy technologies but suffers from low activity. The sluggish four-electron transfer kinetics of OER remains the primary bottleneck in water splitting and metal-air battery technologies. The OER involves multiple proton-coupled electron transfer steps, each with its own activation barrier, making the overall reaction kinetically demanding. Traditional OER catalysts based on noble metal oxides such as IrO2 and RuO2 exhibit high activity but their scarcity and high cost limit large-scale deployment. Consequently, developing earth-abundant and highly active OER electrocatalysts has become a central challenge in the field of renewable energy conversion. The overpotential required to drive OER at practical current densities directly impacts the overall energy efficiency of water electrolysis systems."},
         "confidence": 0.98},
        {"type": "relation", "relation_id": "doc_xxx_r1", "head": "high-entropy alloy",
         "relation_type": "enhances", "relation_surface": "can efficiently activate",
         "tail": "oxygen evolution reaction",
         "evidence": {"section": "Abstract", "original_text": "We reveal that high-entropy alloys (HEAs) can efficiently activate the LOM for enhanced oxygen evolution activity. Density functional theory calculations confirm that the multi-element composition facilitates electron redistribution, lowering the energy barrier for the rate-determining step. The synergistic effect arises from the coexistence of multiple transition metal atoms in the lattice, each contributing distinct electronic states near the Fermi level. This multi-path electron transfer mechanism bypasses the conventional adsorbate evolution mechanism (AEM), which is constrained by the linear scaling relations between intermediate binding energies. As a result, the HEA catalyst achieves an overpotential of only 280 mV at 10 mA/cm², substantially outperforming both IrO2 (320 mV) and RuO2 (310 mV) benchmark catalysts. Electrochemical impedance spectroscopy further confirmed a significantly reduced charge transfer resistance for the HEA compared to the noble metal benchmarks."},
         "confidence": 0.93},
        {"type": "dataset", "dataset_id": "doc_xxx_d1", "name": "OER activity benchmark",
         "modality": "tabular", "domain": "electrochemistry",
         "evidence": {"section": "Results", "original_text": "We benchmark our HEA against state-of-the-art OER catalysts including IrO2 and RuO2. The benchmark dataset comprises overpotential measurements at 10 mA/cm² from 15 independently synthesized electrodes. All measurements were repeated in triplicate to ensure statistical reliability. The dataset also includes Tafel slope values derived from linear sweep voltammetry at a scan rate of 5 mV/s. Electrochemical impedance spectroscopy data were collected at frequencies ranging from 100 kHz to 0.1 Hz with a 10 mV AC amplitude. Chronopotentiometry stability data were recorded at a constant current density of 10 mA/cm² for 24 hours. The raw data files including polarization curves and Nyquist plots are available in the supplementary information."},
         "confidence": 0.90},
        {"type": "method", "method_id": "doc_xxx_m1", "name": "Raman spectroscopy", "method_type": "instrument",
         "evidence": {"section": "Methods", "original_text": "We analyzed the catalyst surface using Raman spectroscopy following the i-t tests in both KOH and TMAOH solutions. Spectra were collected using a 532 nm excitation laser with 5 mW power, integrating 10 scans of 30 seconds each to achieve adequate signal-to-noise ratio. The laser spot size was approximately 1 μm in diameter, allowing spatially resolved mapping of the electrode surface. Baseline correction was performed using a cubic spline interpolation, and peak fitting was carried out with Lorentzian functions. The spectrometer was calibrated using a silicon standard (520.7 cm⁻¹) before each measurement session. Post-electrochemical Raman measurements were conducted ex situ after carefully rinsing the electrode with deionized water and drying under nitrogen flow."},
         "confidence": 0.95},
        {"type": "experiment", "experiment_id": "doc_xxx_x1", "task": "electrochemical stability test",
         "setup": "three-electrode cell, 1M KOH, 298 K, glassy carbon RDE at 1600 rpm",
         "evidence": {"section": "Methods", "original_text": "All electrochemical measurements were performed at 298 K under ambient pressure using a standard three-electrode configuration with a graphite counter electrode and Ag/AgCl reference electrode. All potentials were iR-corrected and calibrated to the reversible hydrogen electrode (RHE) scale. Chronoamperometry was conducted at a constant potential of 1.53 V vs RHE for 24 hours, with the electrolyte continuously purged with O2 to maintain saturation. The working electrode rotation speed was fixed at 1600 rpm to ensure efficient mass transport and rapid removal of evolved oxygen bubbles. The catalyst loading on the glassy carbon electrode was precisely controlled at 0.2 mg/cm². Three independent electrodes were prepared for each catalyst composition to assess batch-to-batch reproducibility."},
         "confidence": 0.95},
        {"type": "performance_result", "perf_id": "doc_xxx_p1",
         "metric": "overpotential at 10 mA/cm²", "compared_to": "IrO2, RuO2",
         "evidence": {"section": "Results", "original_text": "The FeCoNiCrMn HEA exhibits a low overpotential of 280 mV at 10 mA/cm², outperforming IrO2 (320 mV) and RuO2 (310 mV). This represents a 12.5% and 9.7% improvement respectively. The Tafel slope of 45 mV/dec indicates favorable reaction kinetics compared to 68 mV/dec for pure Co3O4. The mass activity of the HEA catalyst at 1.53 V was 120 A/g, which is approximately 3-fold higher than that of IrO2 (40 A/g). Electrochemical impedance spectroscopy revealed a charge transfer resistance of 12 Ω for the HEA, significantly lower than 38 Ω for IrO2, confirming faster electron transfer kinetics at the electrode-electrolyte interface. Stability tests over 1000 cyclic voltammetry cycles showed negligible degradation in overpotential, confirming the robustness of the catalyst under operating conditions."},
         "confidence": 0.95},
        {"type": "quantitative_result", "qr_id": "doc_xxx_qr1", "quantity": "overpotential", "value": 280, "unit": "mV", "context": "FeCoNiCrMn HEA at 10 mA/cm² current density in 1M KOH",
         "result_type": "main_result",
         "evidence": {"section": "Results", "original_text": "The FeCoNiCrMn HEA exhibits a low overpotential of 280 mV at 10 mA/cm², outperforming IrO2 (320 mV) and RuO2 (310 mV). Chronoamperometry measurements at a constant potential of 1.53 V vs RHE confirmed stable current density over 24 hours of continuous operation with less than 3% degradation. The polarization curve was recorded at a slow scan rate of 2 mV/s to minimize capacitive contributions. The overpotential values were determined at the geometric current density of 10 mA/cm², which corresponds to approximately 10% efficient solar-to-fuel conversion. Error bars represent the standard deviation from measurements on five independent electrodes. The improvement is attributed to the multi-path electron transfer mechanism facilitated by configurational entropy."},
         "confidence": 0.97},
        {"type": "quantitative_result", "qr_id": "doc_xxx_qr2", "quantity": "Tafel slope", "value": 45, "unit": "mV/dec", "context": "FeCoNiCrMn HEA in 1M KOH electrolyte",
         "result_type": "measurement",
         "evidence": {"section": "Results", "original_text": "The Tafel slope was measured to be 45 mV/dec, indicating favorable reaction kinetics and suggesting the lattice oxygen mechanism as the dominant pathway. This value is substantially lower than the 68 mV/dec observed for pure Co3O4 under identical conditions. Tafel analysis was performed on the linear region of the polarization curve after iR correction, covering at least one decade of current density. The low Tafel slope implies that the rate-determining step involves the second electron transfer, consistent with the LOM pathway. Complementary pH-dependent measurements confirmed the LOM assignment, as the overpotential showed negligible dependence on electrolyte pH in the range of 12.5 to 14."},
         "confidence": 0.94},
        {"type": "data_specification", "ds_id": "doc_xxx_ds1", "spec_type": "quality_standard",
         "description": "Standardized three-electrode measurement protocol with iR compensation and RHE calibration",
         "evidence": {"section": "Methods", "original_text": "All electrochemical measurements were performed at 298 K under ambient pressure using a standard three-electrode configuration with a graphite counter electrode and Ag/AgCl reference electrode. The working electrode was prepared by drop-casting the catalyst ink onto a glassy carbon rotating disk electrode (0.196 cm²). All potentials were iR-corrected and calibrated to the reversible hydrogen electrode (RHE) scale. The uncompensated resistance was determined by electrochemical impedance spectroscopy at open circuit potential and compensated at 85% level. The electrolyte was 1 M KOH solution prepared with ultrapure water (18.2 MΩ·cm) and purged with high-purity O2 for 30 minutes prior to each experiment. The Ag/AgCl reference electrode was calibrated against a reversible hydrogen electrode in the same electrolyte before and after each measurement session."},
         "confidence": 0.95},
        {"type": "claim", "claim_id": "doc_xxx_ca1",
         "evidence": {"section": "Abstract", "original_text": "Configurational entropy in high-entropy alloys synergistically activates multiple electron transfer pathways, enabling superior OER performance. This finding challenges the conventional wisdom that catalytic activity is solely determined by the electronic structure of individual active sites. The multi-path electron transfer mechanism provides a new paradigm for designing next-generation electrocatalysts. By incorporating multiple transition metal elements into a single-phase solid solution, the catalyst can exploit a continuum of electronic states to facilitate charge transfer at the electrode-electrolyte interface. This concept extends beyond OER catalysis and may be broadly applicable to other multi-electron reactions such as CO2 reduction and nitrogen fixation."},
         "confidence": 0.96},
        {"type": "conclusion", "conclusion_id": "doc_xxx_cl1",
         "evidence": {"section": "Conclusion", "original_text": "High-entropy alloys enable multi-path electron transfer to synergistically activate the lattice oxygen mechanism, providing a new design strategy for efficient OER catalysts. These results demonstrate that configurational complexity can be harnessed as a design parameter to overcome the activity-stability tradeoff that has long plagued OER catalyst development. The FeCoNiCrMn system serves as a model platform, but the design principles established here are generalizable to other HEA compositions. Our work establishes a direct link between configurational entropy, electronic structure, and catalytic activity, opening new avenues for rational catalyst design. The comprehensive electrochemical characterization combined with DFT calculations provides a mechanistic understanding that can guide future catalyst development."},
         "confidence": 0.96},
        {"type": "limitation", "limitation_id": "doc_xxx_lm1",
         "evidence": {"section": "Discussion", "original_text": "The current study is limited to five-component HEAs in alkaline media; generalizability to acid-stable compositions remains to be demonstrated. Furthermore, the long-term stability beyond 24 hours and the performance under practical device conditions (e.g., membrane electrode assemblies) have not been evaluated. The DFT calculations were performed on idealized slab models that do not capture surface reconstruction effects under operating potentials. Additionally, the precise contributions of individual elements to the overall activity cannot be deconvoluted from the present experimental data alone. The catalyst synthesis method yields polycrystalline samples, and the role of specific crystal facets or grain boundaries in the catalytic process warrants further investigation. Finally, the cost and scalability of HEA synthesis compared to conventional binary or ternary catalysts were not assessed."},
         "confidence": 0.92},
        {"type": "future_work", "future_work_id": "doc_xxx_fw1",
         "evidence": {"section": "Discussion", "original_text": "Future studies should explore HEAs in other electrocatalytic reactions such as CO2 reduction and nitrogen reduction. Additionally, machine learning-guided composition screening could accelerate the discovery of optimal HEA formulations. In-situ/operando characterization techniques such as X-ray absorption spectroscopy and surface-enhanced Raman spectroscopy are needed to directly probe the multi-path electron transfer mechanism under working conditions. Systematic investigation of the effect of each constituent element through targeted substitution experiments would help elucidate individual contributions to catalytic activity. Long-term durability testing under industrially relevant current densities exceeding 500 mA/cm² is essential to assess practical viability for commercial electrolyzer applications."},
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

1. **title**：论文的完整标题，必须从论文内容原文中提取，不要改写。预提取标题仅作参考——如果它明显是章节标题（如 \"II. SLUM MAPPING\"）、大小写错乱（如 \"oPeN DATA\"）、作者列表或期刊名，必须忽略并从论文开头找到真正的论文标题
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

## 12 种知识类型

1. **concept**: 关键概念、术语、实体（term/normalized/std_label）
2. **relation**: 概念间语义关系（head/tail 必须对应已抽取的 concept term）
3. **dataset**: 论文使用/产生的数据集（name/modality/domain）
   modality 取值: text | image | tabular | time_series | multimodal | other
4. **method**: 方法、模型、算法、仪器（name/method_type）
   method_type 取值: model | algorithm | protocol | software | instrument | preprocessing
5. **experiment**: 实验设置与流程（task/setup）
6. **performance_result**: 性能对比/评价（metric/compared_to）
7. **quantitative_result**: 科学度量与实验指标（排除年份、页数、编号等元信息）（quantity/value/unit/context/result_type）
   result_type 取值: main_result | baseline | ablation | measurement | threshold
8. **data_specification**: 数据格式规范、质量标准、环境要求（spec_type/description）
   spec_type 取值: format_rule | quality_standard | env_requirement | metadata_standard
9. **conclusion**: 核心结论（仅 evidence）
10. **claim**: 核心主张/发现（仅 evidence）
11. **future_work**: 未来研究方向（仅 evidence）
12. **limitation**: 方法局限、适用约束（仅 evidence）

## 提取原则

1. **忠实性**：original_text 必须是原文直接摘录，禁止改写或总结
2. **完整性**：original_text 必须是完整段落，至少包含 8-10 个完整句子，保留充足的上下文使得读者无需查看原文即可完全理解该知识条目的含义。必须包含实验结果的具体数值、实验条件、对比基准等所有细节
3. **关联性**：relation 的 head/tail 必须对应已抽取的 concept term
4. **轻标注**：concept/dataset/method/experiment 的标注字段值简短
5. **覆盖度**：原文中存在的就全部提取，不要遗漏也不要编造。每组输出 token 上限8000，组内各类型均衡分配
6. **claim/conclusion/limitation/future_work/data_specification** 不是每篇都有，按实际内容抽取
7. **quantitative_result** 应尽可能提取论文中所有出现的主要数值结果，包括图表中报告的数据、消融实验、基线对比等"""

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


# ═══════════════════════════════════════════════════════════════
#  分组提取 Prompt：将 12 种知识类型拆为 5 组串行抽取
#  Group1: concept + relation
#  Group2: dataset + data_specification
#  Group3: method + experiment
#  Group4: quantitative_result + performance_result
#  Group5: conclusion + claim + limitation + future_work
# ═══════════════════════════════════════════════════════════════

# ─── Group1: concept + relation ─────────────────────────────

G1_OUTPUT_EXAMPLE = {
    "entries": [
        {"type": "concept", "concept_id": "doc_xxx_c1", "term": "high-entropy alloy", "normalized": "高熵合金",
         "std_label": "HEA",
         "evidence": {"section": "Abstract",
             "original_text": "We reveal that high-entropy alloys (HEAs) can efficiently activate the LOM through synergistic multi-path electron transfer. Configurational entropy in these multi-principal-element alloys stabilizes a single-phase solid solution, enabling unique catalytic properties not achievable in binary or ternary systems. Unlike conventional alloys that rely on one or two principal elements, HEAs contain five or more principal elements in near-equimolar ratios, creating a vast compositional space. The high configurational entropy lowers the Gibbs free energy, stabilizing disordered solid solution phases over intermetallic compounds. This entropic stabilization has been exploited in various fields including structural materials, catalysis, and energy storage."},
         "confidence": 0.96},
        {"type": "concept", "concept_id": "doc_xxx_c2", "term": "oxygen evolution reaction", "normalized": "氧析出反应",
         "std_label": "OER",
         "evidence": {"section": "Abstract",
             "original_text": "Electrocatalytic oxygen evolution reaction (OER) is key to several energy technologies but suffers from low activity. The sluggish four-electron transfer kinetics of OER remains the primary bottleneck in water splitting and metal-air battery technologies. The OER involves multiple proton-coupled electron transfer steps, each with its own activation barrier, making the overall reaction kinetically demanding. Traditional OER catalysts based on noble metal oxides such as IrO2 and RuO2 exhibit high activity but their scarcity and high cost limit large-scale deployment. Consequently, developing earth-abundant and highly active OER electrocatalysts has become a central challenge in the field of renewable energy conversion."},
         "confidence": 0.98},
        {"type": "relation", "relation_id": "doc_xxx_r1", "head": "high-entropy alloy",
         "relation_type": "enhances", "relation_surface": "can efficiently activate",
         "tail": "oxygen evolution reaction",
         "evidence": {"section": "Abstract",
             "original_text": "We reveal that high-entropy alloys (HEAs) can efficiently activate the LOM for enhanced oxygen evolution activity. Density functional theory calculations confirm that the multi-element composition facilitates electron redistribution, lowering the energy barrier for the rate-determining step. The synergistic effect arises from the coexistence of multiple transition metal atoms in the lattice, each contributing distinct electronic states near the Fermi level. This multi-path electron transfer mechanism bypasses the conventional adsorbate evolution mechanism (AEM), which is constrained by the linear scaling relations between intermediate binding energies. As a result, the HEA catalyst achieves an overpotential of only 280 mV at 10 mA/cm², substantially outperforming both IrO2 (320 mV) and RuO2 (310 mV) benchmark catalysts."},
         "confidence": 0.93},
    ]
}
G1_OUTPUT_EXAMPLE_JSON = json.dumps(G1_OUTPUT_EXAMPLE, ensure_ascii=False, indent=2)

G1_SYSTEM_PROMPT = """你是一位科学文献知识抽取专家。从学术论文中提取概念和概念间关系。

## 输出格式

```json
{output_example}
```

## 知识类型

1. **concept**: 关键概念、术语、实体
   - term: 原文术语
   - normalized: 规范化中文名
   - std_label: 标准缩写（可选）
2. **relation**: 概念间语义关系
   - head/tail 必须对应已抽取的 concept term
   - relation_type: enhances | inhibits | causes | belongs_to | measures | uses | compares | precedes | derives

## 提取原则

1. **忠实性**：original_text 必须是原文直接摘录，禁止改写
2. **完整性**：original_text 必须是完整段落，至少包含 8-10 个完整句子，保留充足上下文
3. **关联性**：relation 的 head/tail 必须对应已抽取的 concept term
4. **覆盖度**：原文中出现的概念全部提取，有明确语义关系的建立 relation。输出 token 上限8000，concept 和 relation 均衡"""

G1_USER_PROMPT = """## 论文内容

{paper_text}

请提取概念和概念间关系。"""


# ─── Group2: dataset + data_specification ─────────────────

G2_OUTPUT_EXAMPLE = {
    "entries": [
        {"type": "dataset", "dataset_id": "doc_xxx_d1", "name": "OER activity benchmark", "modality": "tabular", "domain": "electrochemistry",
         "evidence": {"section": "Results",
             "original_text": "We benchmark our HEA against state-of-the-art OER catalysts including IrO2 and RuO2. The benchmark dataset comprises overpotential measurements at 10 mA/cm² from 15 independently synthesized electrodes. All measurements were repeated in triplicate to ensure statistical reliability. The dataset also includes Tafel slope values derived from linear sweep voltammetry at a scan rate of 5 mV/s. Electrochemical impedance spectroscopy data were collected at frequencies ranging from 100 kHz to 0.1 Hz with a 10 mV AC amplitude. Chronopotentiometry stability data were recorded at a constant current density of 10 mA/cm² for 24 hours."},
         "confidence": 0.90},
        {"type": "data_specification", "ds_id": "doc_xxx_ds1", "spec_type": "quality_standard",
         "description": "Standardized three-electrode measurement protocol with iR compensation and RHE calibration",
         "evidence": {"section": "Methods",
             "original_text": "All electrochemical measurements were performed at 298 K under ambient pressure using a standard three-electrode configuration with a graphite counter electrode and Ag/AgCl reference electrode. All potentials were iR-corrected and calibrated to the reversible hydrogen electrode (RHE) scale. The working electrode was prepared by drop-casting a catalyst ink composed of 5 mg catalyst, 1 mL isopropanol, and 10 μL Nafion onto a glassy carbon rotating disk electrode. The electrolyte was 1 M KOH solution purged with high-purity O2 for at least 30 minutes prior to each experiment. The uncompensated resistance was determined by electrochemical impedance spectroscopy at open circuit potential and compensated at 85% level."},
         "confidence": 0.95},
    ]
}
G2_OUTPUT_EXAMPLE_JSON = json.dumps(G2_OUTPUT_EXAMPLE, ensure_ascii=False, indent=2)

G2_SYSTEM_PROMPT = """你是一位科学文献知识抽取专家。从学术论文中提取数据集和数据规范。

## 输出格式

```json
{output_example}
```

## 知识类型

1. **dataset**: 论文使用/产生的数据集
   - name: 数据集名称
   - modality: 数据模态（可选：text | image | tabular | time_series | multimodal | other）
   - domain: 所属领域（可选）
2. **data_specification**: 数据格式规范、质量标准、环境要求
   - spec_type: format_rule | quality_standard | env_requirement | metadata_standard
   - description: 一句话摘要（可选）

## 提取原则

1. **忠实性**：original_text 必须是原文直接摘录，禁止改写
2. **完整性**：original_text 必须是完整段落，至少包含 8-10 个完整句子，保留充足上下文
3. **覆盖度**：原文中存在的全部提取。输出 token 上限8000，两种类型均衡。切忌编造"""

G2_USER_PROMPT = """## 论文内容

{paper_text}

请提取数据集和数据规范。"""

# ─── Group3: method + experiment ──────────────────────────

G3_OUTPUT_EXAMPLE = {
    "entries": [
        {"type": "method", "method_id": "doc_xxx_m1", "name": "Raman spectroscopy", "method_type": "instrument",
         "evidence": {"section": "Methods",
             "original_text": "We analyzed the catalyst surface using Raman spectroscopy following the i-t tests in both KOH and TMAOH solutions. Spectra were collected using a 532 nm excitation laser with 5 mW power, integrating 10 scans of 30 seconds each to achieve adequate signal-to-noise ratio. The laser spot size was approximately 1 μm in diameter, allowing spatially resolved mapping of the electrode surface. Baseline correction was performed using a cubic spline interpolation, and peak fitting was carried out with Lorentzian functions. The spectrometer was calibrated using a silicon standard (520.7 cm⁻¹) before each measurement session."},
         "confidence": 0.95},
        {"type": "experiment", "experiment_id": "doc_xxx_x1", "task": "electrochemical stability test",
         "setup": "three-electrode cell, 1M KOH, 298 K, glassy carbon RDE at 1600 rpm",
         "evidence": {"section": "Methods",
             "original_text": "All electrochemical measurements were performed at 298 K under ambient pressure using a standard three-electrode configuration. Chronoamperometry was conducted at a constant potential of 1.53 V vs RHE for 24 hours. The electrolyte was continuously purged with O2 to maintain saturation, and the working electrode rotation speed was fixed at 1600 rpm. The catalyst loading on the glassy carbon electrode was precisely controlled at 0.2 mg/cm² to ensure reproducible measurements. Three independent electrodes were prepared for each catalyst composition to assess batch-to-batch reproducibility."},
         "confidence": 0.95},
    ]
}
G3_OUTPUT_EXAMPLE_JSON = json.dumps(G3_OUTPUT_EXAMPLE, ensure_ascii=False, indent=2)

G3_SYSTEM_PROMPT = """你是一位科学文献知识抽取专家。从学术论文中提取方法和实验信息。

## 输出格式

```json
{output_example}
```

## 知识类型

1. **method**: 方法、模型、算法、仪器
   - name: 方法/模型名称
   - method_type: model | algorithm | protocol | software | instrument | preprocessing
2. **experiment**: 实验设置与流程
   - task: 实验任务/名称
   - setup: 实验条件摘要（可选，一句话概括设备、环境、关键参数）

## 提取原则

1. **忠实性**：original_text 必须是原文直接摘录，禁止改写
2. **完整性**：original_text 必须是完整段落，至少包含 8-10 个完整句子，保留充足上下文
3. **覆盖度**：原文中存在的全部提取。输出 token 上限8000，两种类型均衡。切忌编造"""

G3_USER_PROMPT = """## 论文内容

{paper_text}

请提取方法和实验信息。"""

# ─── Group4: quantitative_result + performance_result ─────

G4_OUTPUT_EXAMPLE = {
    "entries": [
        {"type": "quantitative_result", "qr_id": "doc_xxx_qr1", "quantity": "overpotential", "value": 280, "unit": "mV", "context": "FeCoNiCrMn HEA at 10 mA/cm² current density in 1M KOH",
         "result_type": "main_result",
         "evidence": {"section": "Results",
             "original_text": "The FeCoNiCrMn HEA exhibits a low overpotential of 280 mV at 10 mA/cm², outperforming IrO2 (320 mV) and RuO2 (310 mV). Chronoamperometry measurements at a constant potential of 1.53 V vs RHE confirmed stable current density over 24 hours of continuous operation with less than 3% degradation. The polarization curve was recorded at a slow scan rate of 2 mV/s to minimize capacitive contributions. The overpotential values were determined at the geometric current density of 10 mA/cm², which corresponds to approximately 10% efficient solar-to-fuel conversion. Error bars represent the standard deviation from measurements on five independent electrodes. The improvement is attributed to the multi-path electron transfer mechanism facilitated by configurational entropy."},
         "confidence": 0.97},
        {"type": "performance_result", "perf_id": "doc_xxx_p1",
         "metric": "overpotential at 10 mA/cm²", "compared_to": "IrO2, RuO2",
         "evidence": {"section": "Results",
             "original_text": "The FeCoNiCrMn HEA exhibits a low overpotential of 280 mV at 10 mA/cm², outperforming IrO2 (320 mV) and RuO2 (310 mV). This represents a 12.5% and 9.7% improvement respectively. The Tafel slope of 45 mV/dec indicates favorable reaction kinetics compared to 68 mV/dec for pure Co3O4. The mass activity of the HEA catalyst at 1.53 V was 120 A/g, which is approximately 3-fold higher than that of IrO2 (40 A/g). Electrochemical impedance spectroscopy revealed a charge transfer resistance of 12 Ω for the HEA, significantly lower than 38 Ω for IrO2, confirming faster electron transfer kinetics at the electrode-electrolyte interface."},
         "confidence": 0.95},
    ]
}
G4_OUTPUT_EXAMPLE_JSON = json.dumps(G4_OUTPUT_EXAMPLE, ensure_ascii=False, indent=2)

G4_SYSTEM_PROMPT = """你是一位科学文献知识抽取专家。从学术论文中提取量化结果和性能对比。

## 输出格式

```json
{output_example}
```

## 知识类型

1. **quantitative_result**: 科学测量、实验指标、性能数据（排除年份、页数、编号等元信息）
   - quantity: 物理量/指标名称
   - value: 数值（可选）
   - unit: 单位（可选）
   - context: 实验条件/上下文（必填）
   - result_type: main_result | baseline | ablation | measurement | threshold
2. **performance_result**: 性能对比/评价
   - metric: 被比较的指标名称（可选）
   - compared_to: 对比对象（可选）

## 提取原则

1. **证据完整性（最重要）**：每条 evidence 必须是 8-10 句完整段落，保留所有实验条件、对比基准、统计细节。字段（quantity/value/unit/context）只是索引标签，不能替代 evidence。即使量化字段已经概括了结果，evidence 仍必须包含完整原文摘录
2. **忠实性**：original_text 必须是原文直接摘录，禁止改写
3. **质量优先于数量**：只提取有科学意义的测量（排除年份、页数、编号等元信息）。宁可少几条，也要保证每条 evidence 足够详细
4. **覆盖度**：输出 token 上限8000，两种类型均衡"""

G4_USER_PROMPT = """## 论文内容

{paper_text}

请提取量化结果和性能对比。"""

# ─── Group5: conclusion + claim + limitation + future_work ─

G5_OUTPUT_EXAMPLE = {
    "entries": [
        {"type": "claim", "claim_id": "doc_xxx_ca1",
         "evidence": {"section": "Abstract",
             "original_text": "Configurational entropy in high-entropy alloys synergistically activates multiple electron transfer pathways, enabling superior OER performance. This finding challenges the conventional wisdom that catalytic activity is solely determined by the electronic structure of individual active sites. The multi-path electron transfer mechanism provides a new paradigm for designing next-generation electrocatalysts. By incorporating multiple transition metal elements into a single-phase solid solution, the catalyst can exploit a continuum of electronic states to facilitate charge transfer at the electrode-electrolyte interface."},
         "confidence": 0.96},
        {"type": "conclusion", "conclusion_id": "doc_xxx_cl1",
         "evidence": {"section": "Conclusion",
             "original_text": "High-entropy alloys enable multi-path electron transfer to synergistically activate the lattice oxygen mechanism, providing a new design strategy for efficient OER catalysts. These results demonstrate that configurational complexity can be harnessed as a design parameter to overcome the activity-stability tradeoff that has long plagued OER catalyst development. The FeCoNiCrMn system serves as a model platform, but the design principles established here are generalizable to other HEA compositions. Our work establishes a direct link between configurational entropy, electronic structure, and catalytic activity."},
         "confidence": 0.96},
        {"type": "limitation", "limitation_id": "doc_xxx_lm1",
         "evidence": {"section": "Discussion",
             "original_text": "The current study is limited to five-component HEAs in alkaline media; generalizability to acid-stable compositions remains to be demonstrated. Furthermore, the long-term stability beyond 24 hours and the performance under practical device conditions have not been evaluated. The DFT calculations were performed on idealized slab models that do not capture surface reconstruction effects under operating potentials. Additionally, the precise contributions of individual elements to the overall activity cannot be deconvoluted from the present experimental data alone."},
         "confidence": 0.92},
        {"type": "future_work", "future_work_id": "doc_xxx_fw1",
         "evidence": {"section": "Discussion",
             "original_text": "Future studies should explore HEAs in other electrocatalytic reactions such as CO2 reduction and nitrogen reduction. Additionally, machine learning-guided composition screening could accelerate the discovery of optimal HEA formulations. In-situ/operando characterization techniques such as X-ray absorption spectroscopy are needed to directly probe the multi-path electron transfer mechanism under working conditions. Long-term durability testing under industrially relevant current densities exceeding 500 mA/cm² is essential to assess practical viability."},
         "confidence": 0.93},
    ]
}
G5_OUTPUT_EXAMPLE_JSON = json.dumps(G5_OUTPUT_EXAMPLE, ensure_ascii=False, indent=2)

G5_SYSTEM_PROMPT = """你是一位科学文献知识抽取专家。从学术论文中提取核心主张、结论、局限性和未来工作。

## 输出格式

```json
{output_example}
```

## 知识类型

1. **claim**: 核心主张/发现 — 仅需 evidence
2. **conclusion**: 核心结论 — 仅需 evidence
3. **limitation**: 方法局限、适用约束 — 仅需 evidence
4. **future_work**: 未来研究方向 — 仅需 evidence

## 提取原则

1. **忠实性**：original_text 必须是原文直接摘录，禁止改写
2. **完整性**：original_text 必须是完整段落，至少包含 8-10 个完整句子，保留充足上下文
3. **区分度**：claim 是核心论点/假设，conclusion 是经实验验证后的结论
4. **覆盖度**：原文有的全部提取，没有的不编造。四种类型均衡。输出 token 上限8000"""

G5_USER_PROMPT = """## 论文内容

{paper_text}

请提取核心主张、结论、局限性和未来工作。"""

# ─── 分组 Prompt 构建函数 ────────────────────────────────────────

def build_grouped_extraction_prompts(paper_text: str) -> list[tuple[str, str, str]]:
    """构建 5 组分类型提取 prompt，返回 [(group_name, sys_prompt, user_prompt), ...]"""
    return [
        ("G1_concept_relation",
         G1_SYSTEM_PROMPT.format(output_example=G1_OUTPUT_EXAMPLE_JSON),
         G1_USER_PROMPT.format(paper_text=paper_text)),
        ("G2_dataset_spec",
         G2_SYSTEM_PROMPT.format(output_example=G2_OUTPUT_EXAMPLE_JSON),
         G2_USER_PROMPT.format(paper_text=paper_text)),
        ("G3_method_experiment",
         G3_SYSTEM_PROMPT.format(output_example=G3_OUTPUT_EXAMPLE_JSON),
         G3_USER_PROMPT.format(paper_text=paper_text)),
        ("G4_quant_perf",
         G4_SYSTEM_PROMPT.format(output_example=G4_OUTPUT_EXAMPLE_JSON),
         G4_USER_PROMPT.format(paper_text=paper_text)),
        ("G5_insight_outlook",
         G5_SYSTEM_PROMPT.format(output_example=G5_OUTPUT_EXAMPLE_JSON),
         G5_USER_PROMPT.format(paper_text=paper_text)),
    ]
