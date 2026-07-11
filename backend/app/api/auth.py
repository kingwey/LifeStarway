from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.schemas.auth import Token, RegisterRequest, LoginRequest, UserResponse
from app.services import register, login
from app.utils.deps import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse)
async def register_user(request: RegisterRequest, db: AsyncSession = Depends(get_db)):
    user = await register(db, request)
    return user


@router.post("/login", response_model=Token)
async def login_user(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    token = await login(db, request)
    return token


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(user: User = Depends(get_current_user)):
    return user
