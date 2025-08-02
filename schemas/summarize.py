from pydantic import BaseModel, Field
from typing import List, Optional


class ArticleRequest(BaseModel):
    text: str = Field(..., description="요약할 뉴스 기사 텍스트")


class SummarizeResponse(BaseModel):
    summary: str = Field(..., description="요약된 텍스트")


class ReportFeatures(BaseModel):
    """제보의 특징 정보"""
    accident_types: List[str] = Field(default=[], description="감지된 사고/사건 유형")
    time_info: List[str] = Field(default=[], description="발생 시간 정보")
    location_info: List[str] = Field(default=[], description="발생 장소 정보")
    is_urgent: bool = Field(default=False, description="긴급 여부")
    damage_info: dict = Field(default={}, description="피해 정보")


class ReportRequest(BaseModel):
    text: str = Field(..., description="요약할 제보 텍스트")
    include_features: bool = Field(default=False, description="제보 특징 정보 포함 여부")


class ReportResponse(BaseModel):
    summary: str = Field(..., description="요약된 제보 텍스트")
    features: Optional[ReportFeatures] = Field(default=None, description="제보 특징 정보")
    urgency_level: str = Field(default="일반", description="긴급도 레벨") 