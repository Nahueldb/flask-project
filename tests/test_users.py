from tests.conftest import app, client
from app.users.models import User
from app.users.schemas import UserCreateSchema, UserUpdateSchema
from app.core.error_handlers import UserNotFoundError, UserAlreadyExistsError
import pytest


def test_create_user(client):
    # Test creating a user
    user_data = UserCreateSchema(username="testcreateuser", email="testcreateuser@mail.com")
    response = client.post('api/users/', json=user_data.model_dump())
    assert response.status_code == 201
    assert response.json['status'] == 'user created successfully'
    assert response.json['user']['username'] == user_data.username
    assert response.json['user']['email'] == user_data.email


def test_update_user(client):
    # First create a user to update
    user_data = UserCreateSchema(username="testupdateuser", email="testupdateuser@mail.com")
    response = client.post('api/users/', json=user_data.model_dump())
    assert response.status_code == 201
    user_id = response.json['user']['id']
    assert user_id is not None
    # Now update the user
    update_data = UserUpdateSchema(username="updateduser", email="updateuser@mail.com")
    response = client.put(f'api/users/{user_id}', json=update_data.model_dump())
    assert response.status_code == 200
    assert response.json['status'] == 'updated successfully'
    assert response.json['user']['username'] == update_data.username
    assert response.json['user']['email'] == update_data.email


def test_get_users(client):
    # GIVEN: no users exist
    response = client.get('/api/users/')
    assert response.status_code == 200
    assert response.json == []

    # WHEN: two users are created
    user1 = UserCreateSchema(username="testcreateuser", email="test1@mail.com")
    user2 = UserCreateSchema(username="testcreateuser2", email="test2@mail.com")
    client.post('/api/users/', json=user1.model_dump())
    client.post('/api/users/', json=user2.model_dump())

    # THEN: the GET request should return them
    response = client.get('/api/users/')
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert len(response.json) == 2

    usernames = [u['username'] for u in response.json]
    assert user1.username in usernames
    assert user2.username in usernames


def test_create_user_already_exists(client):
    # First create a user
    user_data = UserCreateSchema(username="testuserexists", email="testuserexists@mail.com")
    response = client.post('api/users/', json=user_data.model_dump())
    assert response.status_code == 201
    # Now try to create the same user again
    response = client.post('api/users/', json=user_data.model_dump())
    assert response.status_code == 409
    assert response.json['error'] == 'User already exists'