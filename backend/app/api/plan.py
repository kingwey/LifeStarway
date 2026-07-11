from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.schemas.plan import PlanResponse, PlanCreate
from app.services import generate_plan, get_plans, get_plan
from app.utils.deps import get_current_user

router = APIRouter(prefix="/plans", tags=["plans"])


@router.post("/generate", response_model=PlanResponse)
async def generate_plan_api(
    request: PlanCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    plan = await generate_plan(db, str(user.id), request.plan_type, request.diagnosis_id)
    return plan


@router.get("", response_model=list[PlanResponse])
async def get_plans_api(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    plans = await get_plans(db, str(user.id))
    return plans


@router.get("/{plan_id}", response_model=PlanResponse)
async def get_plan_api(
    plan_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    plan = await get_plan(db, str(user.id), plan_id)
    return plan
