from pydantic import BaseModel, Field
from typing import List, Optional


class SimulationCreate(BaseModel):
    hypothesis: dict = Field(default_factory=dict)
    profile_id: Optional[str] = None


class SimulationResponse(BaseModel):
    id: str
    user_id: str
    profile_id: str
    hypothesis: dict = Field(default_factory=dict)
    simulated_milestones: List[dict] = Field(default_factory=list)
    risk_assessment: dict = Field(default_factory=dict)
    comparison: dict = Field(default_factory=dict)
    created_at: str

    class Config:
        orm_mode = True
