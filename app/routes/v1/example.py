from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError as MarshmallowValidationError
from app.extensions import limiter, db
from app.utils.sanitizer import sanitize_dict
from app.utils.permissions import require_permission
from app.modules.example.model import ExampleCreate, ExampleRead
from app.modules.example.service import ExampleService
from app.errors.handlers import ValidationError
from app.database.schema import User

example_bp = Blueprint("example", __name__, url_prefix="/example")

service = ExampleService()
read_schema = ExampleRead()
create_schema = ExampleCreate()


@example_bp.route("", methods=["GET"])
@jwt_required()
@limiter.limit("30 per minute")
def list_examples():
    return jsonify(read_schema.dump(service.get_all(), many=True)), 200


@example_bp.route("/<int:user_id>", methods=["GET"])
@jwt_required()
@limiter.limit("30 per minute")
def get_example(user_id):
    return jsonify(read_schema.dump(service.get_by_id(user_id))), 200


@example_bp.route("", methods=["POST"])
@require_permission("example.create")  # layer 1: role-permission check
@limiter.limit("10 per minute")
def create_example():
    try:
        data = create_schema.load(sanitize_dict(request.json or {}))
    except MarshmallowValidationError as e:
        raise ValidationError(message=e.messages)
    return jsonify(read_schema.dump(service.create(**data))), 201


@example_bp.route("/<int:user_id>", methods=["DELETE"])
@require_permission("example.delete")  # layer 1: role-permission check
@limiter.limit("10 per minute")
def delete_example(user_id):
    actor = db.session.get(User, get_jwt_identity())
    # layer 2: ExamplePolicy().delete(actor, target) would go here
    service.delete(user_id)
    return jsonify({"message": "Deleted successfully"}), 200
