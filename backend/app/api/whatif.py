from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.schemas.simulation import SimulationCreate, SimulationResponse
from app.services import create_simulation, get_simulation, get_simulations
from app.utils.deps import get_current_user

router = APIRouter(prefix="/simulations", tags=["simulations"])


@router.post("", response_model=SimulationResponse)
async def create_simulation_api(
    request: SimulationCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    simulation = await create_simulation(db, str(user.id), request.hypothesis, request.profile_id)
    return simulation


@router.get("/{sim_id}", response_model=SimulationResponse)
async def get_simulation_api(
    sim_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    simulation = await get_simulation(db, str(user.id), sim_id)
    return simulation


@router.get("", response_model=list[SimulationResponse])
async def get_simulations_api(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    simulations = await get_simulations(db, str(user.id))
    return simulations
