from app.users.models import User
from flask import jsonify, request, Blueprint
from app.core.db import db
from app.users.schemas import UserSchema, UserCreateSchema, UserUpdateSchema
from pydantic import ValidationError

user_bp = Blueprint('users', __name__)


@user_bp.route('/', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([UserSchema.model_validate(user).model_dump() for user in users])


@user_bp.route('/', methods=['POST'])
def create_user():
    try:
        data = UserCreateSchema(**request.get_json())
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400

    user_exists = User.query.filter_by(username=data.username).first()
    if user_exists:
        return jsonify({'error': 'User already exists'}), 400
    user = User(username=data.username, email=data.email)

    db.session.add(user)
    db.session.commit()
    return jsonify({
        'status': 'user created successfully',
        'user': UserSchema.model_validate(user).model_dump()
        }), 201


@user_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)

    try:
        data = UserUpdateSchema(**request.get_json())
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400

    user.username = data.username if data.username is not None else user.username
    user.email = data.email if data.email is not None else user.email
    db.session.commit()
    return jsonify({
        'status': 'updated successfully',
        'user': UserSchema.model_validate(user).model_dump()
        }), 200
