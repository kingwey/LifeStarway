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
    id: str
    user_id: str
    diagnosis_id: str
    plan_type: str
    title: str
    description: str
    milestones: List[Milestone] = Field(default_factory=list)
    recommended_path: dict = Field(default_factory=dict)
    alternative_paths: List[dict] = Field(default_factory=list)
    created_at: str

    model_config = {"from_attributes": True}


class PlanListResponse(BaseModel):
    items: List[PlanResponse]
    total: int
    skip: int
    limit: int