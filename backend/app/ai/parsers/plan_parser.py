import json
import re
from typing import Dict, Any

from pydantic import BaseModel, ValidationError
from typing import List


class DiagnosisResult(BaseModel):
    health_score: float
    dimensions: Dict[str, float]
    strengths: List[str]
    risks: List[str]
    summary: str


class Milestone(BaseModel):
    id: str
    title: str
    target_date: str
    category: str
    metrics: Dict[str, Any] = {}
    probability: float
    position: Dict[str, float] = {}


class PlanResult(BaseModel):
    title: str
    description: str
    milestones: List[Milestone] = []
    recommended_path: Dict[str, Any] = {}
    alternative_paths: List[Dict[str, Any]] = []


class ResumeResult(BaseModel):
    birth_year: int | None = None
    gender: str | None = None
    education: str | None = None
    major: str | None = None
    school: str | None = None
    skills: List[Dict[str, Any]] = []
    personality_type: str | None = None
    current_industry: str | None = None
    current_role: str | None = None
    work_years: int | None = None
    salary_range: str | None = None
    career_history: List[Dict[str, Any]] = []
    resume_text: str | None = None


class WhatIfResult(BaseModel):
    simulated_milestones: List[Dict[str, Any]] = []
    risk_assessment: Dict[str, Any] = {}
    comparison: Dict[str, Any] = {}


def extract_json(text: str) -> str:
    match = re.search(r'\{[\s\S]*\}', text)
    if match:
        return match.group()
    return text


def parse_llm_diagnosis(raw_output: str) -> DiagnosisResult:
    try:
        json_str = extract_json(raw_output)
        data = json.loads(json_str)
        return DiagnosisResult(**data)
    except (json.JSONDecodeError, ValidationError) as e:
        raise RuntimeError(f"诊断结果解析失败: {str(e)}")


def parse_llm_plan(raw_output: str) -> PlanResult:
    try:
        json_str = extract_json(raw_output)
        data = json.loads(json_str)
        return PlanResult(**data)
    except (json.JSONDecodeError, ValidationError) as e:
        raise RuntimeError(f"规划结果解析失败: {str(e)}")


def parse_llm_resume(raw_output: str) -> ResumeResult:
    try:
        json_str = extract_json(raw_output)
        data = json.loads(json_str)
        return ResumeResult(**data)
    except (json.JSONDecodeError, ValidationError) as e:
        raise RuntimeError(f"简历解析失败: {str(e)}")


def parse_llm_whatif(raw_output: str) -> WhatIfResult:
    try:
        json_str = extract_json(raw_output)
        data = json.loads(json_str)
        return WhatIfResult(**data)
    except (json.JSONDecodeError, ValidationError) as e:
        raise RuntimeError(f"What-If模拟解析失败: {str(e)}")
