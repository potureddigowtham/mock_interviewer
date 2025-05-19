from flask import jsonify, request, current_app
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity, get_jwt
)
from werkzeug.exceptions import BadRequest, Unauthorized, Conflict

from ...models import db, User, UserRole
from .. import api_bp


@api_bp.route('/auth/register', methods=['POST'])
def register():
    """Register a new user."""
    data = request.get_json()
    
    # Validate input
    if not all(k in data for k in ['username', 'email', 'password']):
        raise BadRequest('Missing required fields')
    
    # Check if username or email already exists
    if User.query.filter_by(username=data['username']).first():
        raise Conflict('Username already exists')
    if User.query.filter_by(email=data['email']).first():
        raise Conflict('Email already registered')
    
    # Create new user with candidate role by default
    user = User(
        username=data['username'],
        email=data['email'],
        role=UserRole.CANDIDATE
    )
    user.password = data['password']  # This will hash the password
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        'message': 'User registered successfully',
        'user': user.to_dict()
    }), 201


@api_bp.route('/auth/login', methods=['POST'])
def login():
    """Login user and return JWT tokens."""
    data = request.get_json()
    
    if not all(k in data for k in ['username', 'password']):
        raise BadRequest('Username and password are required')
    
    user = User.query.filter_by(username=data['username']).first()
    
    if not user or not user.verify_password(data['password']):
        raise Unauthorized('Invalid username or password')
    
    if not user.is_active:
        raise Unauthorized('Account is deactivated')
    
    # Create tokens
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    
    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': user.to_dict()
    }), 200


@api_bp.route('/auth/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Refresh access token."""
    current_user_id = get_jwt_identity()
    access_token = create_access_token(identity=current_user_id)
    return jsonify({'access_token': access_token}), 200


@api_bp.route('/auth/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current user's profile."""
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())


@api_bp.route('/auth/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """Change user's password."""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not all(k in data for k in ['current_password', 'new_password']):
        raise BadRequest('Current and new password are required')
    
    user = User.query.get_or_404(user_id)
    
    if not user.verify_password(data['current_password']):
        raise Unauthorized('Current password is incorrect')
    
    user.password = data['new_password']
    db.session.commit()
    
    return jsonify({'message': 'Password updated successfully'}), 200


# Admin-only endpoints
@api_bp.route('/admin/users', methods=['GET'])
@jwt_required()
def list_users():
    """List all users (admin only)."""
    current_user_id = get_jwt_identity()
    current_user = User.query.get_or_404(current_user_id)
    
    if current_user.role != UserRole.ADMIN:
        raise Unauthorized('Admin access required')
    
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])


@api_bp.route('/admin/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    """Update user details (admin only)."""
    current_user_id = get_jwt_identity()
    current_user = User.query.get_or_404(current_user_id)
    
    if current_user.role != UserRole.ADMIN:
        raise Unauthorized('Admin access required')
    
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    
    if 'role' in data:
        try:
            user.role = UserRole(data['role'])
        except ValueError:
            raise BadRequest('Invalid role')
    
    if 'is_active' in data:
        user.is_active = bool(data['is_active'])
    
    db.session.commit()
    
    return jsonify(user.to_dict())
