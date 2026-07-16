from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.schemas.diagnosis import DiagnosisResponse, DiagnosisCreate, DiagnosisListResponse
from app.services import create_diagnosis, get_latest_diagnosis, get_diagnoses, get_diagnoses_count
from app.utils.deps import get_current_user

router = APIRouter(prefix="/diagnoses", tags=["diagnoses"])


@router.post("", response_model=DiagnosisResponse)
async def create_diagnosis_api(
    request: DiagnosisCreate = None,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    profile_id = request.profile_id if request else None
    diagnosis = await create_diagnosis(db, str(user.id), profile_id)
    return diagnosis


@router.get("/latest", response_model=DiagnosisResponse)
async def get_latest_diagnosis_api(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    diagnosis = await get_latest_diagnosis(db, str(user.id))
    return diagnosis


@router.get("", response_model=DiagnosisListResponse)
async def get_diagnoses_api(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    diagnoses = await get_diagnoses(db, str(user.id), skip=skip, limit=limit)
    total = await get_diagnoses_count(db, str(user.id))
    return {"items": diagnoses, "total": total, "skip": skip, "limit": limit}