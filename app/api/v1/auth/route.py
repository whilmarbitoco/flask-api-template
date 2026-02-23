from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.modules.auth.controller import AuthController
from app.extensions import limiter
from app.utils.sanitizer import sanitize_dict

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
controller = AuthController()

@auth_bp.route('/register', methods=['POST'])
@limiter.limit("5 per hour")
def register():
    sanitized_data = sanitize_dict(request.json or {})
    result = controller.register_user(sanitized_data)
    return jsonify(result), 201

@auth_bp.route('/login', methods=['POST'])
@limiter.limit("10 per minute")
def login():
    sanitized_data = sanitize_dict(request.json or {})
    result = controller.login_user(sanitized_data)
    
    response = make_response(jsonify({
        "access_token": result['access_token'],
        "user": result['user']
    }), 200)
    
    response.set_cookie(
        'refresh_token',
        value=result['refresh_token'],
        httponly=True,
        secure=True,
        samesite='Strict',
        max_age=30*24*60*60
    )
    
    return response

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()
    result = controller.refresh_access_token(user_id)
    return jsonify(result), 200

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    response = make_response(jsonify({"message": "Logged out successfully"}), 200)
    response.set_cookie('refresh_token', '', expires=0)
    return response
