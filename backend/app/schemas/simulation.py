from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional


class SimulationCreate(BaseModel):
    hypothesis: dict = Field(default_factory=dict)
    profile_id: Optional[str] = None


class SimulationResponse(BaseModel):
    id: UUID
    user_id: UUID
    profile_id: UUID
    hypothesis: dict = Field(default_factory=dict)
    simulated_milestones: List[dict] = Field(default_factory=list)
    risk_assessment: dict = Field(default_factory=dict)
    comparison: dict = Field(default_factory=dict)
    created_at: datetime

    model_config = {"from_attributes": True}
