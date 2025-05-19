from datetime import datetime, timedelta
from enum import Enum
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
import jwt
from server.app import db

class UserRole(Enum):
    CANDIDATE = "candidate"
    ADMIN = "admin"

class User(db.Model):
    """User model for authentication and authorization."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.Enum(UserRole), nullable=False, default=UserRole.CANDIDATE)
    is_active = db.Column(db.Boolean(), default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            self.role = UserRole.CANDIDATE

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        """Set password hash from plaintext password."""
        if len(password) < 8:
            raise ValueError('Password must be at least 8 characters long')
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """Check if provided password matches the stored hash."""
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expires_in=3600):
        """Generate JWT token for the user."""
        payload = {
            'user_id': self.id,
            'role': self.role.value,
            'exp': datetime.utcnow() + timedelta(seconds=expires_in)
        }
        return jwt.encode(
            payload,
            current_app.config.get('JWT_SECRET_KEY', 'dev-jwt-secret'),
            algorithm='HS256'
        )

    @staticmethod
    def verify_auth_token(token):
        """Verify JWT token and return user if valid."""
        try:
            data = jwt.decode(
                token,
                current_app.config.get('JWT_SECRET_KEY', 'dev-jwt-secret'),
                algorithms=['HS256']
            )
        except:
            return None
        return User.query.get(data['user_id'])

    def has_role(self, role_name):
        """Check if user has the specified role."""
        return self.role == UserRole[role_name.upper()]

    def to_dict(self):
        """Return user data as dictionary."""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role.value,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def __repr__(self):
        return f'<User {self.username} ({self.role.value})>'
