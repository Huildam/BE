from pydantic import BaseModel, EmailStr
from typing import Optional


class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    email: str
    role: str
    region_id: Optional[int] = None


class UserResponse(BaseModel):
    id: int
    email: str
    role: str
    region_id: Optional[int] = None
    created_at: str 