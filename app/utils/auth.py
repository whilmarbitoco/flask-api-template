from functools import wraps
from flask import request
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from app.errors.handlers import UnauthorizedError, ForbiddenError

def jwt_required_custom(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
            return fn(*args, **kwargs)
        except Exception as e:
            raise UnauthorizedError(message="Invalid or missing authentication token")
    return wrapper

def admin_required(fn):
    """Require admin role from JWT claims"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims.get("role") != "admin":
            raise ForbiddenError(message="Admin access required")
        return fn(*args, **kwargs)
    return wrapper
