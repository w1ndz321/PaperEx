"""
kg_schema.py — 知识抽取的 Pydantic 模型定义

12 种知识类型: concept, relation, dataset, method, experiment,
              performance_result, quantitative_result, data_specification,
              conclusion, claim, future_work, limitation
"""

from typing import Optional, List, Literal
from pydantic import BaseModel, Field


class Evidence(BaseModel):
    section: str
    original_text: str


class Concept(BaseModel):
    type: Literal["concept"] = "concept"
    concept_id: str
    term: str
    normalized: str
    std_label: Optional[str] = None
    evidence: Evidence
    confidence: float = Field(..., ge=0.0, le=1.0)


class Relation(BaseModel):
    type: Literal["relation"] = "relation"
    relation_id: str
    head: str
    head_term: str
    relation_type: str
    relation_surface: str
    tail: str
    tail_term: str
    evidence: Evidence
    confidence: float = Field(..., ge=0.0, le=1.0)


class Dataset(BaseModel):
    type: Literal["dataset"] = "dataset"
    dataset_id: str
    name: str
    modality: Optional[Literal["text", "image", "tabular", "time_series", "multimodal", "other"]] = None
    domain: Optional[str] = None
    evidence: Evidence
    confidence: float = Field(..., ge=0.0, le=1.0)


class Method(BaseModel):
    type: Literal["method"] = "method"
    method_id: str
    name: str
    method_type: Literal["model", "algorithm", "protocol", "software", "instrument", "preprocessing"]
    evidence: Evidence
    confidence: float = Field(..., ge=0.0, le=1.0)


class Experiment(BaseModel):
    type: Literal["experiment"] = "experiment"
    experiment_id: str
    task: str
    setup: Optional[str] = None
    evidence: Evidence
    confidence: float = Field(..., ge=0.0, le=1.0)


class PerformanceResult(BaseModel):
    type: Literal["performance_result"] = "performance_result"
    perf_id: str
    metric: Optional[str] = None
    compared_to: Optional[str] = None
    evidence: Evidence
    confidence: float = Field(..., ge=0.0, le=1.0)


class QuantitativeResult(BaseModel):
    type: Literal["quantitative_result"] = "quantitative_result"
    qr_id: str
    quantity: str
    value: Optional[float] = None
    unit: Optional[str] = None
    context: str
    result_type: Literal["main_result", "baseline", "ablation", "measurement", "threshold"]
    evidence: Evidence
    confidence: float = Field(..., ge=0.0, le=1.0)


class DataSpecification(BaseModel):
    type: Literal["data_specification"] = "data_specification"
    ds_id: str
    spec_type: Literal["format_rule", "quality_standard", "env_requirement", "metadata_standard"]
    description: Optional[str] = None
    evidence: Evidence
    confidence: float = Field(..., ge=0.0, le=1.0)


class Conclusion(BaseModel):
    type: Literal["conclusion"] = "conclusion"
    conclusion_id: str
    evidence: Evidence
    confidence: float = Field(..., ge=0.0, le=1.0)


class Claim(BaseModel):
    type: Literal["claim"] = "claim"
    claim_id: str
    evidence: Evidence
    confidence: float = Field(..., ge=0.0, le=1.0)


class FutureWork(BaseModel):
    type: Literal["future_work"] = "future_work"
    future_work_id: str
    evidence: Evidence
    confidence: float = Field(..., ge=0.0, le=1.0)


class Limitation(BaseModel):
    type: Literal["limitation"] = "limitation"
    limitation_id: str
    evidence: Evidence
    confidence: float = Field(..., ge=0.0, le=1.0)


Entry = Concept | Relation | Dataset | Method | Experiment | PerformanceResult | QuantitativeResult | DataSpecification | Conclusion | Claim | FutureWork | Limitation


class DisciplineLevel(BaseModel):
    level1: Optional[str] = None
    level2: Optional[str] = None
    level3: Optional[str] = None


class ExtractionInfo(BaseModel):
    extraction_model: str
    extraction_timestamp: str


class Metadata(BaseModel):
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


class ExtractionOutput(BaseModel):
    metadata: Metadata
    entries: List[Entry] = []


class LLMExtractionResponse(BaseModel):
    entries: Optional[List[dict]] = None
    concepts: List[dict] = []
    relations: List[dict] = []
    datasets: List[dict] = []
    methods: List[dict] = []
    experiments: List[dict] = []
    performances: List[dict] = []
    quantitative_results: List[dict] = []
    data_specifications: List[dict] = []
    conclusions: List[dict] = []
    claims: List[dict] = []
    future_works: List[dict] = []
    limitations: List[dict] = []
    model_config = {"extra": "allow"}


class LLMDisciplineResponse(BaseModel):
    title: Optional[str] = None
    year: Optional[int] = None
    doi: Optional[str] = None
    primary_discipline: dict = {}
    secondary_disciplines: Optional[List[dict]] = None
    keywords: List[str] = []
