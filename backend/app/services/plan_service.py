from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import json

from app.models.profile import Profile
from app.models.diagnosis import Diagnosis
from app.models.plan import Plan
from app.schemas.diagnosis import DiagnosisResponse
from app.schemas.plan import PlanResponse
from app.ai import call_llm, DIAGNOSIS_PROMPT, PLANNING_PROMPT, PLAN_TYPE_DESCS, parse_llm_diagnosis, parse_llm_plan


async def create_diagnosis(db: AsyncSession, user_id: str, profile_id: str = None):
    if not profile_id:
        result = await db.execute(select(Profile).where(Profile.user_id == user_id))
        profile = result.scalar_one_or_none()
        if not profile:
            raise HTTPException(status_code=400, detail="请先创建人生档案")
    else:
        result = await db.execute(select(Profile).where(Profile.id == profile_id))
        profile = result.scalar_one_or_none()
        if not profile or str(profile.user_id) != user_id:
            raise HTTPException(status_code=404, detail="档案不存在")
    
    profile_data = {
        "学历": profile.education or "",
        "专业": profile.major or "",
        "学校": profile.school or "",
        "技能": json.dumps(profile.skills, ensure_ascii=False) if profile.skills else "[]",
        "性格类型": profile.personality_type or "",
        "当前行业": profile.current_industry or "",
        "当前职位": profile.current_role or "",
        "工作年限": profile.work_years or 0,
        "薪资区间": profile.salary_range or "",
        "工作履历": json.dumps(profile.career_history, ensure_ascii=False) if profile.career_history else "[]"
    }
    
    try:
        prompt = DIAGNOSIS_PROMPT.format(profile_data=json.dumps(profile_data, ensure_ascii=False))
        raw_output = await call_llm(prompt)
        parsed = parse_llm_diagnosis(raw_output)
    except Exception as e:
        logger = __import__('logging').getLogger('lifestarway.diagnosis')
        logger.warning(f"LLM诊断失败: {e}")
        raise HTTPException(status_code=500, detail="职业诊断生成失败，请稍后重试")
    
    diagnosis = Diagnosis(
        user_id=user_id,
        profile_id=str(profile.id),
        profile_version=profile.version,
        health_score=parsed.health_score,
        dimensions=parsed.dimensions,
        strengths=parsed.strengths,
        risks=parsed.risks,
        summary=parsed.summary
    )
    
    db.add(diagnosis)
    await db.commit()
    await db.refresh(diagnosis)
    return diagnosis


async def get_latest_diagnosis(db: AsyncSession, user_id: str):
    result = await db.execute(
        select(Diagnosis).where(Diagnosis.user_id == user_id).order_by(Diagnosis.created_at.desc()).limit(1)
    )
    return result.scalar_one_or_none()


async def get_diagnoses(db: AsyncSession, user_id: str):
    result = await db.execute(
        select(Diagnosis).where(Diagnosis.user_id == user_id).order_by(Diagnosis.created_at.desc())
    )
    return result.scalars().all()


async def generate_plan(db: AsyncSession, user_id: str, plan_type: str, diagnosis_id: str = None):
    if plan_type not in PLAN_TYPE_DESCS:
        raise HTTPException(status_code=400, detail="无效的规划类型")
    
    if not diagnosis_id:
        diagnosis = await get_latest_diagnosis(db, user_id)
        if not diagnosis:
            raise HTTPException(status_code=400, detail="请先进行职业诊断")
    else:
        result = await db.execute(select(Diagnosis).where(Diagnosis.id == diagnosis_id))
        diagnosis = result.scalar_one_or_none()
        if not diagnosis or str(diagnosis.user_id) != user_id:
            raise HTTPException(status_code=404, detail="诊断不存在")
    
    result = await db.execute(select(Profile).where(Profile.id == diagnosis.profile_id))
    profile = result.scalar_one_or_none()
    if not profile:
        raise HTTPException(status_code=404, detail="档案不存在")
    
    profile_data = {
        "学历": profile.education or "",
        "专业": profile.major or "",
        "学校": profile.school or "",
        "技能": json.dumps(profile.skills, ensure_ascii=False) if profile.skills else "[]",
        "性格类型": profile.personality_type or "",
        "当前行业": profile.current_industry or "",
        "当前职位": profile.current_role or "",
        "工作年限": profile.work_years or 0,
        "薪资区间": profile.salary_range or "",
        "工作履历": json.dumps(profile.career_history, ensure_ascii=False) if profile.career_history else "[]"
    }
    
    diagnosis_data = {
        "健康度": diagnosis.health_score,
        "各维度": diagnosis.dimensions,
        "优势": diagnosis.strengths,
        "风险": diagnosis.risks,
        "总结": diagnosis.summary
    }
    
    try:
        prompt = PLANNING_PROMPT.format(
            plan_type=plan_type,
            plan_type_desc=PLAN_TYPE_DESCS[plan_type],
            profile_data=json.dumps(profile_data, ensure_ascii=False),
            diagnosis_data=json.dumps(diagnosis_data, ensure_ascii=False)
        )
        raw_output = await call_llm(prompt)
        parsed = parse_llm_plan(raw_output)
    except Exception as e:
        logger = __import__('logging').getLogger('lifestarway.plan')
        logger.warning(f"LLM规划失败: {e}")
        raise HTTPException(status_code=500, detail="职业规划生成失败，请稍后重试")
    
    plan = Plan(
        user_id=user_id,
        diagnosis_id=str(diagnosis.id),
        plan_type=plan_type,
        title=parsed.title,
        description=parsed.description,
        milestones=[m.dict() for m in parsed.milestones],
        recommended_path=parsed.recommended_path,
        alternative_paths=parsed.alternative_paths
    )
    
    db.add(plan)
    await db.commit()
    await db.refresh(plan)
    return plan


async def get_plans(db: AsyncSession, user_id: str):
    result = await db.execute(select(Plan).where(Plan.user_id == user_id).order_by(Plan.created_at.desc()))
    return result.scalars().all()


async def get_plan(db: AsyncSession, user_id: str, plan_id: str):
    result = await db.execute(select(Plan).where(Plan.id == plan_id))
    plan = result.scalar_one_or_none()
    if not plan or str(plan.user_id) != user_id:
        raise HTTPException(status_code=404, detail="规划不存在")
    return plan