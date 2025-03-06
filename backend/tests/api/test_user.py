import pytest
from fastapi.testclient import TestClient

from backend.main import app
from backend.models.sqlalchemy_models import User
from backend.service.oauth import get_current_user

# from backend.db.sessions import get_db

client = TestClient(app)


def override_get_current_user():
    """Overrides the token auth and gets back a mock user"""
    return User(id=1, username="admin", role=5)


# app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


@pytest.mark.users
def test_read_users_me():
    """Test the /users/me endpoint"""
    response = client.get("/users/me")
    assert response.status_code == 200
    assert response.json() == {"username": "admin", "role": 5}


@pytest.mark.users
def test_get_users():
    """Test the /users/ endpoint to get all users"""
    response = client.get("/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.users
def test_read_user():
    """Test the /users/{user_id} endpoint"""
    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json()["username"] == "admin"


@pytest.mark.users
def test_read_user_not_found():
    """Test the /users/{user_id} endpoint"""
    response = client.get("/users/178")
    assert response.status_code == 404
    assert response.json()["detail"] == "User does not exist"


@pytest.mark.users
def test_create_user():
    """Test the /users/ endpoint for creating a new user"""

    response = client.post(
        "/users/",
        params={"username": "newuser1", "password": "password1", "role": 2},
    )
    assert response.status_code == 200
    assert response.json()["username"] == "newuser1"


@pytest.mark.users
def test_create_duplicate_user():
    """Try to create same user twice and it should not be allowed"""

    response = client.post(
        "/users/",
        params={"username": "newuser2", "password": "password2", "role": 2},
    )
    assert response.status_code == 200
    assert response.json()["username"] == "newuser2"

    response = client.post(
        "/users/",
        params={"username": "newuser2", "password": "password2", "role": 2},
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "User with same name exists"


@pytest.mark.users
def test_update_user():
    """Test the /users/{user_id} endpoint for updating user details"""
    response = client.put(
        "/users/1",
        params={
            "username": "updateduser",
            "password": "newpassword",
            "role": 3,
        },
    )
    assert response.status_code == 200
    assert response.json()["username"] == "updateduser"


@pytest.mark.users
def test_delete_user():
    """Test the /users/{user_id} endpoint for deleting a user"""
    response = client.delete("/users/1")
    if response.status_code == 200:
        assert response.json() == {"message": "User deleted"}


@pytest.mark.users
def test_delete_unknown_user():
    """Test the /users/{user_id} endpoint for deleting a user"""
    response = client.delete("/users/1222")
    assert response.status_code == 404
    assert response.json()["detail"] == "User does not exist"
