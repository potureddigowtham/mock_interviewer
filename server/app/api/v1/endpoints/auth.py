"""Authentication endpoints."""
from datetime import timedelta
import sys
from typing import Dict, Any, Optional

# Handle Python version compatibility
try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

from .... import models, schemas
from ....core import security
from ....core.config import settings
from ....db.base import get_db
from ...deps import get_current_user

router = APIRouter()

@router.post("/login/access-token", response_model=schemas.Token)
async def login_access_token(
    db: Annotated[Session, Depends(get_db)],
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> dict:
    """OAuth2 compatible token login, get an access token for future requests."""
    user = db.query(models.User).filter(
        models.User.username == form_data.username
    ).first()
    
    if not user or not user.verify_password(form_data.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.post("/login/test-token", response_model=schemas.User)
async def test_token(
    current_user: Annotated[models.User, Depends(get_current_user)],
) -> models.User:
    """Test access token."""
    return current_user

@router.post("/register", response_model=schemas.User)
def create_user(
    user_in: schemas.UserCreate,
    db: Annotated[Session, Depends(get_db)],
) -> models.User:
    """Create new user."""
    # Check if user with this email already exists
    db_user = db.query(models.User).filter(
        models.User.email == user_in.email
    ).first()
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    # Check if username is taken
    db_user = db.query(models.User).filter(
        models.User.username == user_in.username
    ).first()
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Username already registered"
        )
    
    # Create new user
    hashed_password = security.get_password_hash(user_in.password)
    db_user = models.User(
        email=user_in.email,
        username=user_in.username,
        hashed_password=hashed_password,
        full_name=user_in.full_name,
        role=models.UserRole.CANDIDATE
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user
