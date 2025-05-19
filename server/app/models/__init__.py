"""Database models package."""
from .user import User, UserRole
from .base import Base  # noqa

# Import all models here to ensure they are registered with SQLAlchemy
__all__ = ["User", "UserRole", "Base"]
