"""
kg_schema.py — 知识抽取的 Pydantic 模型定义

用于验证 LLM 输出的结构化数据
"""

from typing import Optional, List, Literal, Union
from pydantic import BaseModel, Field, field_validator


# ─── Evidence 基础模型 ────────────────────────────────────────

class Evidence(BaseModel):
    """证据字段"""
    section: str = Field(..., description="章节名称")
    original_text: str = Field(..., description="原文片段")


# ─── Metadata 模型 ────────────────────────────────────────────

class DisciplineLevel(BaseModel):
    """学科层级"""
    level1: Optional[str] = None
    level2: Optional[str] = None
    level3: Optional[str] = None


class ExtractionInfo(BaseModel):
    """抽取信息"""
    extraction_model: str
    extraction_timestamp: str


class Metadata(BaseModel):
    """论文元数据"""
    title: Optional[str] = None
    year: Optional[int] = None
    doi: Optional[str] = None
    doc_id: str
    abstract: str = ""
    introduction: str = ""
    primary_discipline: DisciplineLevel
    secondary_disciplines: Optional[List[DisciplineLevel]] = None
    keywords: List[str] = []
    extraction_info: ExtractionInfo


# ─── 8 种知识类型模型 ──────────────────────────────────────────

# 1. concept
class Concept(BaseModel):
    """概念"""
    type: Literal["concept"] = "concept"
    concept_id: str
    term: str
    normalized: str
    std_label: Optional[str] = None
    evidence: Evidence
    confidence: float = Field(..., ge=0.0, le=1.0)


# 2. relation
class Relation(BaseModel):
    """关系"""
    type: Literal["relation"] = "relation"
    relation_id: str
    head: str
    head_term: str
    relation_type: str
    relation_surface: str
    tail: str
    tail_term: str
    direction: Literal["directed", "undirected"] = "directed"
    evidence: Evidence
    confidence: float = Field(..., ge=0.0, le=1.0)


# 3. dataset_and_benchmark
class DatasetItem(BaseModel):
    """数据集项"""
    name: str
    role: Literal["used", "produced", "referenced"]
    samples: Optional[int] = None
    domain: Optional[str] = None
    data_format: Optional[str] = None
    task_type: Optional[str] = None


class DatasetAndBenchmark(BaseModel):
    """数据集与基准"""
    type: Literal["dataset_and_benchmark"] = "dataset_and_benchmark"
    dataset_id: str
    datasets: List[DatasetItem]
    evidence: Evidence
    confidence: float = Field(..., ge=0.0, le=1.0)


# 4. method_and_experiment
class MethodItem(BaseModel):
    """方法项"""
    name: str
    method_type: Literal["model", "algorithm", "protocol", "software", "instrument", "preprocessing"]
    category: Optional[str] = None


class Experiment(BaseModel):
    """实验设置"""
    task: str
    dataset_ref: Optional[str] = None
    method_ref: Optional[str] = None


class MethodAndExperiment(BaseModel):
    """方法与实验"""
    type: Literal["method_and_experiment"] = "method_and_experiment"
    method_id: str
    methods: List[MethodItem]
    experiment: Optional[Experiment] = None
    evidence: Evidence
    confidence: float = Field(..., ge=0.0, le=1.0)


# 5. performance_result
class MetricItem(BaseModel):
    """指标项"""
    name: str
    value: float
    unit: Optional[str] = None
    method_ref: Optional[str] = None
    dataset_ref: Optional[str] = None


class PerformanceResult(BaseModel):
    """性能结果"""
    type: Literal["performance_result"] = "performance_result"
    perf_id: str
    metrics: List[MetricItem]
    evidence: Evidence
    confidence: float = Field(..., ge=0.0, le=1.0)


# 6. experimental_parameter
class ParameterItem(BaseModel):
    """参数项"""
    name: str
    value: float
    unit: Optional[str] = None
    param_type: Literal["env_condition", "operating_condition", "material_property", "time_duration", "threshold"]


class ExperimentalParameter(BaseModel):
    """实验参数与物理量"""
    type: Literal["experimental_parameter"] = "experimental_parameter"
    param_id: str
    parameters: List[ParameterItem]
    evidence: Evidence
    confidence: float = Field(..., ge=0.0, le=1.0)


# 7. data_specification
class DataSpecification(BaseModel):
    """数据规范与标准"""
    type: Literal["data_specification"] = "data_specification"
    spec_id: str
    spec_type: Literal["format_rule", "quality_standard", "env_requirement", "metadata_standard"]
    related_formats: Optional[List[str]] = None
    related_domain: Optional[str] = None
    evidence: Evidence
    confidence: float = Field(..., ge=0.0, le=1.0)


# 8. conclusion_and_insight
class ConclusionAndInsight(BaseModel):
    """结论与洞见"""
    type: Literal["conclusion_and_insight"] = "conclusion_and_insight"
    insight_id: str
    insight_type: Literal["conclusion", "limitation", "future_direction", "optimization_strategy", "domain_insight"]
    evidence: Evidence
    confidence: float = Field(..., ge=0.0, le=1.0)


# ─── Entry 联合类型 ────────────────────────────────────────────

Entry = Union[
    Concept,
    Relation,
    DatasetAndBenchmark,
    MethodAndExperiment,
    PerformanceResult,
    ExperimentalParameter,
    DataSpecification,
    ConclusionAndInsight,
]


# ─── 完整输出模型 ──────────────────────────────────────────────

class ExtractionOutput(BaseModel):
    """完整抽取输出"""
    metadata: Metadata
    entries: List[Entry] = []

    @field_validator('entries', mode='before')
    @classmethod
    def validate_entries(cls, v):
        """验证并过滤无效条目"""
        validated = []
        for item in v:
            try:
                entry_type = item.get('type')
                if entry_type == 'concept':
                    validated.append(Concept(**item))
                elif entry_type == 'relation':
                    validated.append(Relation(**item))
                elif entry_type == 'dataset_and_benchmark':
                    validated.append(DatasetAndBenchmark(**item))
                elif entry_type == 'method_and_experiment':
                    validated.append(MethodAndExperiment(**item))
                elif entry_type == 'performance_result':
                    validated.append(PerformanceResult(**item))
                elif entry_type == 'experimental_parameter':
                    validated.append(ExperimentalParameter(**item))
                elif entry_type == 'data_specification':
                    validated.append(DataSpecification(**item))
                elif entry_type == 'conclusion_and_insight':
                    validated.append(ConclusionAndInsight(**item))
            except Exception:
                # 跳过无效条目
                continue
        return validated


# ─── LLM 输出模型（用于解析原始 LLM 响应）──────────────────────

class LLMConceptOutput(BaseModel):
    """LLM 概念输出"""
    term: str
    normalized: str = ""
    std_label: Optional[str] = None
    evidence: dict = {}
    confidence: float = 0.9


class LLMRelationOutput(BaseModel):
    """LLM 关系输出"""
    head: str
    head_term: str = ""
    relation_type: str
    relation_surface: str
    tail: str
    tail_term: str = ""
    direction: str = "directed"
    evidence: dict = {}
    confidence: float = 0.9


class LLMDatasetOutput(BaseModel):
    """LLM 数据集输出"""
    datasets: List[dict] = []
    evidence: dict = {}
    confidence: float = 0.9


class LLMMethodOutput(BaseModel):
    """LLM 方法输出"""
    methods: List[dict] = []
    experiment: Optional[dict] = None
    evidence: dict = {}
    confidence: float = 0.9


class LLMPerformanceOutput(BaseModel):
    """LLM 性能输出"""
    metrics: List[dict] = []
    evidence: dict = {}
    confidence: float = 0.9


class LLMParameterOutput(BaseModel):
    """LLM 参数输出"""
    parameters: List[dict] = []
    evidence: dict = {}
    confidence: float = 0.9


class LLMSpecificationOutput(BaseModel):
    """LLM 规范输出"""
    spec_type: str
    related_formats: Optional[List[str]] = None
    related_domain: Optional[str] = None
    evidence: dict = {}
    confidence: float = 0.9


class LLMInsightOutput(BaseModel):
    """LLM 洞见输出"""
    insight_type: str
    evidence: dict = {}
    confidence: float = 0.9


class LLMExtractionResponse(BaseModel):
    """LLM 抽取响应 - 支持两种格式：
    1. 新格式：{"entries": [...]}
    2. 旧格式：{"concepts": [...], "relations": [...], ...}
    """
    entries: Optional[List[dict]] = None
    # 旧格式字段（兼容）
    concepts: List[dict] = []
    relations: List[dict] = []
    datasets: List[dict] = []
    methods: List[dict] = []
    performances: List[dict] = []
    parameters: List[dict] = []
    specifications: List[dict] = []
    insights: List[dict] = []

    model_config = {"extra": "allow"}  # 允许额外字段


class LLMDisciplineResponse(BaseModel):
    """LLM 学科分类响应"""
    primary_discipline: dict = {}
    secondary_disciplines: Optional[List[dict]] = None
    keywords: List[str] = []