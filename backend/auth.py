import jwt
import bcrypt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, current_app
from models import User

def hash_password(password):
    """Generate bcrypt hash for password storage"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password, hashed_password):
    """Compare plain password with stored hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def generate_token(user_id, username, role):
    """Create JWT access token with user information and expiration"""
    payload = {
        'user_id': user_id,
        'username': username,
        'role': role,
        'exp': datetime.utcnow() + timedelta(hours=1),  # Token expires in 1 hour
        'iat': datetime.utcnow()  # Issued at timestamp
    }
    return jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')

def verify_token(token):
    """Validate JWT token and extract payload"""
    try:
        payload = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token has expired
    except jwt.InvalidTokenError:
        return None  # Token is malformed or invalid

def token_required(f):
    """Decorator to enforce JWT authentication on routes"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Extract token from Authorization header (format: "Bearer <token>")
        if 'Authorization' in request.headers:
            try:
                token = request.headers['Authorization'].split(" ")[1]
            except:
                return jsonify({'message': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        # Verify token and attach user info to request object
        payload = verify_token(token)
        if not payload:
            return jsonify({'message': 'Token is invalid or expired'}), 401
        
        request.user_id = payload['user_id']
        request.username = payload['username']
        request.user_role = payload['role']
        
        return f(*args, **kwargs)
    
    return decorated

def admin_required(f):
    """Decorator to restrict route access to administrators only"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not hasattr(request, 'user_role') or request.user_role != 'admin':
            return jsonify({'message': 'Admin access required'}), 403
        return f(*args, **kwargs)
    
    return decorated

def user_required(f):
    """Decorator to allow access to both regular users and administrators"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not hasattr(request, 'user_role') or request.user_role not in ['user', 'admin']:
            return jsonify({'message': 'User access required'}), 403
        return f(*args, **kwargs)
    
    return decorated 