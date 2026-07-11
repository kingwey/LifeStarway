from pydantic import BaseModel, Field
from typing import Optional, List


class Skill(BaseModel):
    name: str
    level: str
    years: float


class CareerItem(BaseModel):
    company: str
    role: str
    period: str
    salary: Optional[str] = None


class ProfileCreate(BaseModel):
    birth_year: Optional[int] = None
    gender: Optional[str] = None
    education: Optional[str] = None
    major: Optional[str] = None
    school: Optional[str] = None
    skills: List[Skill] = Field(default_factory=list)
    personality_type: Optional[str] = None
    current_industry: Optional[str] = None
    current_role: Optional[str] = None
    work_years: Optional[int] = None
    salary_range: Optional[str] = None
    career_history: List[CareerItem] = Field(default_factory=list)
    resume_text: Optional[str] = None


class ProfileUpdate(ProfileCreate):
    pass


class ProfileResponse(ProfileCreate):
    id: str
    user_id: str
    version: int
    created_at: str
    updated_at: Optional[str] = None

    class Config:
        orm_mode = True


class ResumeImportRequest(BaseModel):
    resume_text: str


class ResumeImportResponse(BaseModel):
    success: bool
    profile_data: ProfileCreate
