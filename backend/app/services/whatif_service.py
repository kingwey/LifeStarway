from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import json

from app.models.profile import Profile
from app.models.simulation import Simulation
from app.ai import call_llm, WHATIF_PROMPT, parse_llm_whatif


async def create_simulation(db: AsyncSession, user_id: str, hypothesis: dict, profile_id: str = None):
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
        prompt = WHATIF_PROMPT.format(
            profile_data=json.dumps(profile_data, ensure_ascii=False),
            hypothesis=json.dumps(hypothesis, ensure_ascii=False)
        )
        raw_output = await call_llm(prompt)
        parsed = parse_llm_whatif(raw_output)
    except Exception as e:
        logger = __import__('logging').getLogger('lifestarway.whatif')
        logger.warning(f"LLM模拟失败: {e}")
        raise HTTPException(status_code=500, detail="模拟分析失败，请稍后重试")
    
    simulation = Simulation(
        user_id=user_id,
        profile_id=str(profile.id),
        hypothesis=hypothesis,
        simulated_milestones=parsed.simulated_milestones,
        risk_assessment=parsed.risk_assessment,
        comparison=parsed.comparison
    )
    
    db.add(simulation)
    await db.commit()
    await db.refresh(simulation)
    return simulation


async def get_simulation(db: AsyncSession, user_id: str, sim_id: str):
    result = await db.execute(select(Simulation).where(Simulation.id == sim_id))
    sim = result.scalar_one_or_none()
    if not sim or str(sim.user_id) != user_id:
        raise HTTPException(status_code=404, detail="模拟记录不存在")
    return sim


async def get_simulations(db: AsyncSession, user_id: str):
    result = await db.execute(select(Simulation).where(Simulation.user_id == user_id).order_by(Simulation.created_at.desc()))
    return result.scalars().all()