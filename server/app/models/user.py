"""User model and related functionality."""
from enum import Enum
from typing import Optional

from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import relationship

from .base import Base

class UserRole(str, Enum):
    """User roles in the system."""
    ADMIN = "admin"
    CANDIDATE = "candidate"
    INTERVIEWER = "interviewer"


class User(Base):
    """User model for authentication and authorization.
    
    Attributes:
        email: User's email address (unique)
        username: Username (unique)
        hashed_password: Hashed password
        full_name: User's full name
        role: User role (admin, candidate, or interviewer)
        is_active: Whether the user is active
    """
    __tablename__ = 'users'
    
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=True)
    role = Column(String(20), default=UserRole.CANDIDATE.value, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Relationships will be added later when the related models exist
    # interviews = relationship("Interview", back_populates="candidate")
    # feedback = relationship("Feedback", back_populates="interviewer")
    
    def set_password(self, password: str) -> None:
        """Set hashed password.
        
        Args:
            password: Plain text password to hash and store
        """
        from ..core.security import get_password_hash
        self.hashed_password = get_password_hash(password)
    
    def check_password(self, password: str) -> bool:
        """Check if the provided password matches the stored hash.
        
        Args:
            password: Plain text password to verify
            
        Returns:
            bool: True if the password matches, False otherwise
        """
        from ..core.security import verify_password
        return verify_password(password, self.hashed_password)

    def __repr__(self) -> str:
        """String representation of the User model."""
        return f"<User {self.email}>"
