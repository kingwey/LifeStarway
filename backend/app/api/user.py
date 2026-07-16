from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.schemas.auth import UserUpdate, PasswordUpdate, UserResponse
from app.utils.deps import get_current_user, verify_password, get_password_hash

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(user: User = Depends(get_current_user)):
    return user


@router.patch("/me", response_model=UserResponse)
async def update_user_info(
    data: UserUpdate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if data.nickname:
        user.nickname = data.nickname
    await db.commit()
    await db.refresh(user)
    return user


@router.post("/me/password")
async def update_password(
    data: PasswordUpdate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if not verify_password(data.old_password, user.hashed_password):
        raise HTTPException(status_code=400, detail="原密码错误")
    
    user.hashed_password = get_password_hash(data.new_password)
    await db.commit()
    return {"success": True, "message": "密码修改成功"}