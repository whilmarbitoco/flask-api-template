from flask import Blueprint, request, jsonify
from app.modules.users.controller import UserController
from app.utils.auth import jwt_required_custom
from app.utils.sanitizer import sanitize_dict
from app.extensions import limiter

users_bp = Blueprint('users', __name__, url_prefix='/users')
controller = UserController()

@users_bp.route('', methods=['GET'])
@jwt_required_custom
@limiter.limit("30 per minute")
def list_users():
    users = controller.list_users(request.args)
    return jsonify(users), 200

@users_bp.route('', methods=['POST'])
@jwt_required_custom
@limiter.limit("10 per minute")
def create_user():
    sanitized_data = sanitize_dict(request.json or {})
    user = controller.create_user(sanitized_data)
    return jsonify(user), 201

@users_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required_custom
@limiter.limit("30 per minute")
def get_user(user_id):
    user = controller.get_user(user_id)
    return jsonify(user), 200