from flask import jsonify, request, Blueprint
from app.core.db import db
from app.users.schemas import UserSchema, UserCreateSchema, UserUpdateSchema
from app.users.services import UserService
from app.core.error_handlers import UserNotFoundError, UserAlreadyExistsError

user_bp = Blueprint('users', __name__)


@user_bp.route('/', methods=['GET'])
def get_users():
    users = UserService.get_users()
    if not users:
        raise UserNotFoundError()
    return jsonify([UserSchema.model_validate(user).model_dump() for user in users])


@user_bp.route('/', methods=['POST'])
def create_user():
    data = UserCreateSchema(**request.get_json())

    user_exists = UserService.get_user_by_username(data.username)
    if user_exists:
        raise UserAlreadyExistsError(data.username)

    user = UserService.create_user(data.username, data.email)

    return jsonify({
        'status': 'user created successfully',
        'user': UserSchema.model_validate(user).model_dump()
        }), 201


@user_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = UserService.get_user_by_id(user_id)
    if not user:
        raise UserNotFoundError()

    data = UserUpdateSchema(**request.get_json())

    user = UserService.update_user(
        user,
        username=data.username if data.username is not None else user.username,
        email=data.email if data.email is not None else user.email
    )
    return jsonify({
        'status': 'updated successfully',
        'user': UserSchema.model_validate(user).model_dump()
        }), 200
