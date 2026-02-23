from flask import Blueprint, request, jsonify
from app.modules.users.controller import UserController

users_bp = Blueprint('users', __name__, url_prefix='/users')
controller = UserController()

@users_bp.route('', methods=['GET'])
def list_users():
    users = controller.list_users(request.args)
    return jsonify(users), 200

@users_bp.route('', methods=['POST'])
def create_user():
    user = controller.create_user(request.json)
    return jsonify(user), 201

@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = controller.get_user(user_id)
    return jsonify(user), 200