# Import models here to avoid circular imports
from server.app import db
from .user import User, UserRole

__all__ = ['db', 'User', 'UserRole']
