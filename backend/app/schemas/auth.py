from uuid import UUID
from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: str | None = None


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    nickname: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    nickname: str

    model_config = {"from_attributes": True}
