from tests.conftest import app, client
from app.users.models import User
from app.users.schemas import UserCreateSchema, UserUpdateSchema
from app.core.error_handlers import UserNotFoundError, UserAlreadyExistsError
import pytest


def test_user(client):
    # Test creating a user
    user_data = UserCreateSchema(username="testuser", email="testuser@mail.com")
    response = client.post('api/users/', json=user_data.model_dump())
    assert response.status_code == 201
    assert response.json['status'] == 'user created successfully'
    assert response.json['user']['username'] == user_data.username
    assert response.json['user']['email'] == user_data.email
