"""Token related schemas."""
from typing import Optional, List
from pydantic import BaseModel, Field

class Token(BaseModel):
    """Token response schema."""
    access_token: str
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    """Token payload schema."""
    sub: Optional[str] = None
    exp: Optional[int] = None

class TokenData(BaseModel):
    """Token data schema."""
    username: Optional[str] = None
    scopes: List[str] = []
