"""User related schemas."""
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, EmailStr, Field, validator

from ..models.user import UserRole

class UserBase(BaseModel):
    """Base user schema."""
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50, pattern=r"^[a-zA-Z0-9_-]+$")
    full_name: Optional[str] = Field(None, min_length=1, max_length=100)

class UserCreate(UserBase):
    """Schema for user creation."""
    password: str = Field(..., min_length=8, max_length=100)

class UserUpdate(BaseModel):
    """Schema for user updates."""
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=50, pattern=r"^[a-zA-Z0-9_-]+$")
    full_name: Optional[str] = Field(None, min_length=1, max_length=100)
    password: Optional[str] = Field(None, min_length=8, max_length=100)
    is_active: Optional[bool] = None

class UserInDBBase(UserBase):
    """Base schema for user in database."""
    id: int
    is_active: bool
    role: UserRole
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True  # For backwards compatibility with older Pydantic versions

class UserInDB(UserInDBBase):
    """Schema for user in database with hashed password."""
    hashed_password: str

class User(UserInDBBase):
    """Schema for user response."""
    pass
