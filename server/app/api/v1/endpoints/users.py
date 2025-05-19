"""User management endpoints."""
from typing import List

# Handle Python version compatibility
try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .... import models, schemas
from ....core.config import settings
from ....db.base import get_db
from ...deps import get_current_active_user, get_current_admin

router = APIRouter()

@router.get("/me", response_model=schemas.User)
async def read_user_me(
    current_user: Annotated[models.User, Depends(get_current_active_user)],
) -> models.User:
    """Get current user."""
    return current_user

@router.put("/me", response_model=schemas.User)
def update_user_me(
    user_in: schemas.UserUpdate,
    current_user: Annotated[models.User, Depends(get_current_active_user)],
    db: Annotated[Session, Depends(get_db)],
) -> models.User:
    """Update current user."""
    user_data = user_in.dict(exclude_unset=True)
    
    # If password is being updated, hash it
    if "password" in user_data:
        hashed_password = security.get_password_hash(user_data["password"])
        del user_data["password"]
        user_data["hashed_password"] = hashed_password
    
    # Update user fields
    for field, value in user_data.items():
        setattr(current_user, field, value)
    
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    
    return current_user

# Admin only endpoints
@router.get("/", response_model=List[schemas.User])
def read_users(
    skip: int = 0,
    limit: int = 100,
    current_user: Annotated[models.User, Depends(get_current_admin)] = None,
    db: Annotated[Session, Depends(get_db)] = None,
) -> List[models.User]:
    """Retrieve users (admin only)."""
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users

@router.get("/{user_id}", response_model=schemas.User)
def read_user(
    user_id: int,
    current_user: Annotated[models.User, Depends(get_current_admin)],
    db: Annotated[Session, Depends(get_db)],
) -> models.User:
    """Get a specific user by ID (admin only)."""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@router.put("/{user_id}", response_model=schemas.User)
def update_user(
    user_id: int,
    user_in: schemas.UserUpdate,
    current_user: Annotated[models.User, Depends(get_current_admin)],
    db: Annotated[Session, Depends(get_db)],
) -> models.User:
    """Update a user (admin only)."""
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user_data = user_in.dict(exclude_unset=True)
    
    # If password is being updated, hash it
    if "password" in user_data:
        hashed_password = security.get_password_hash(user_data["password"])
        del user_data["password"]
        user_data["hashed_password"] = hashed_password
    
    # Update user fields
    for field, value in user_data.items():
        setattr(db_user, field, value)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    current_user: Annotated[models.User, Depends(get_current_admin)],
    db: Annotated[Session, Depends(get_db)],
) -> None:
    """Delete a user (admin only)."""
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    db.delete(db_user)
    db.commit()
    return None
