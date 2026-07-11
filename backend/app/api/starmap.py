from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.schemas.starmap import StarMapResponse
from app.services import get_starmap_data
from app.utils.deps import get_current_user

router = APIRouter(prefix="/starmap", tags=["starmap"])


@router.get("", response_model=StarMapResponse)
async def get_starmap_api(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    data = await get_starmap_data(db, str(user.id))
    return data
