import re
from uuid import UUID
from pydantic import BaseModel, EmailStr, field_validator


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: str | None = None


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    nickname: str

    @field_validator('password')
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError('密码长度至少为8位')
        if not re.search(r'[a-z]', v):
            raise ValueError('密码必须包含小写字母')
        if not re.search(r'[A-Z]', v):
            raise ValueError('密码必须包含大写字母')
        if not re.search(r'[0-9]', v):
            raise ValueError('密码必须包含数字')
        if not re.search(r'[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>/?]', v):
            raise ValueError('密码必须包含特殊字符')
        return v


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    nickname: str

    model_config = {"from_attributes": True}
