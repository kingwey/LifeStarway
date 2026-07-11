from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.schemas.profile import ProfileCreate, ProfileResponse, ResumeImportRequest, ResumeImportResponse
from app.services import get_profile, create_or_update_profile, import_resume, get_profile_versions
from app.utils.deps import get_current_user

router = APIRouter(prefix="/profiles", tags=["profiles"])


@router.get("", response_model=ProfileResponse)
async def get_user_profile(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    profile = await get_profile(db, str(user.id))
    return profile


@router.post("", response_model=ProfileResponse)
async def update_profile(
    data: ProfileCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    profile = await create_or_update_profile(db, str(user.id), data)
    return profile


@router.post("/import-resume", response_model=ResumeImportResponse)
async def import_resume_text(
    request: ResumeImportRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    profile_data = await import_resume(db, str(user.id), request.resume_text)
    return {"success": True, "profile_data": profile_data}


@router.get("/versions", response_model=list[ProfileResponse])
async def get_profile_version_history(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    versions = await get_profile_versions(db, str(user.id))
    return versions
