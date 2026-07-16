from uuid import UUID
from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional


class Dimensions(BaseModel):
    growth: float
    stability: float
    income_potential: float
    interest_match: float
    industry_outlook: float


class DiagnosisCreate(BaseModel):
    profile_id: Optional[str] = None


class DiagnosisResponse(BaseModel):
    id: UUID
    user_id: UUID
    profile_id: UUID
    profile_version: int
    health_score: float
    dimensions: Dimensions
    strengths: List[str]
    risks: List[str]
    summary: str
    created_at: datetime

    model_config = {"from_attributes": True}


class DiagnosisListResponse(BaseModel):
    items: List[DiagnosisResponse]
    total: int
    skip: int
    limit: int