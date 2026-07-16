from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional


class Milestone(BaseModel):
    id: str
    title: str
    target_date: str
    category: str
    metrics: dict = Field(default_factory=dict)
    probability: float
    position: dict = Field(default_factory=dict)


class PlanCreate(BaseModel):
    plan_type: str
    diagnosis_id: Optional[str] = None


class PlanResponse(BaseModel):
    id: UUID
    user_id: UUID
    diagnosis_id: UUID
    plan_type: str
    title: str
    description: str
    milestones: List[Milestone] = Field(default_factory=list)
    recommended_path: dict = Field(default_factory=dict)
    alternative_paths: List[dict] = Field(default_factory=list)
    created_at: datetime

    model_config = {"from_attributes": True}


class PlanListResponse(BaseModel):
    items: List[PlanResponse]
    total: int
    skip: int
    limit: int