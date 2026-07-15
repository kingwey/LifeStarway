from fastapi import HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.profile import Profile
from app.schemas.profile import ProfileCreate, ProfileUpdate
from app.ai import call_llm, RESUME_PARSE_PROMPT, parse_llm_resume


async def get_profile(db: AsyncSession, user_id: str):
    result = await db.execute(select(Profile).where(Profile.user_id == user_id))
    profile = result.scalar_one_or_none()
    return profile


async def create_or_update_profile(db: AsyncSession, user_id: str, data: ProfileCreate):
    result = await db.execute(select(Profile).where(Profile.user_id == user_id))
    existing = result.scalar_one_or_none()
    
    if existing:
        existing.version += 1
        for key, value in data.dict(exclude_unset=True).items():
            setattr(existing, key, value)
        await db.commit()
        await db.refresh(existing)
        return existing
    
    new_profile = Profile(
        user_id=user_id,
        **data.dict(exclude_unset=True)
    )
    db.add(new_profile)
    await db.commit()
    await db.refresh(new_profile)
    return new_profile


async def import_resume(db: AsyncSession, user_id: str, resume_text: str):
    try:
        prompt = RESUME_PARSE_PROMPT.format(resume_text=resume_text[:2000])
        raw_output = await call_llm(prompt)
        parsed = parse_llm_resume(raw_output)
        
        profile_data = ProfileCreate(
            birth_year=parsed.birth_year,
            gender=parsed.gender,
            education=parsed.education,
            major=parsed.major,
            school=parsed.school,
            skills=parsed.skills,
            personality_type=parsed.personality_type,
            current_industry=parsed.current_industry,
            current_role=parsed.current_role,
            work_years=parsed.work_years,
            salary_range=parsed.salary_range,
            career_history=parsed.career_history,
            resume_text=resume_text
        )
    except Exception as e:
        logger = __import__('logging').getLogger('lifestarway.profile')
        logger.warning(f"LLM解析失败，返回原始数据: {e}")
        profile_data = ProfileCreate(resume_text=resume_text)
    
    profile = await create_or_update_profile(db, user_id, profile_data)
    return profile_data


async def get_profile_versions(db: AsyncSession, user_id: str):
    result = await db.execute(
        select(Profile).where(Profile.user_id == user_id).order_by(Profile.version.desc())
    )
    return result.scalars().all()
