from typing import Optional
from pydantic import BaseModel, EmailStr

class UserRegister(BaseModel):
    email: EmailStr
    phone: Optional[str] = None
    password: str
    full_name: str
    role: str = "MEMBER"
    preferred_language: str = "en"
    district_id: Optional[str] = None
    cooperative_id: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class PasswordChange(BaseModel):
    old_password: str
    new_password: str
