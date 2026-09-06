import pytest
from app import create_app, db


@pytest.fixture()
def client():
    app = create_app()
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
        JWT_SECRET_KEY="test-secret",
    )

    with app.app_context():
        db.drop_all()
        db.create_all()

    with app.test_client() as client:
        yield client

    with app.app_context():
        db.session.remove()
        db.drop_all()


def test_register_success(client):
    response = client.post(
        "/register",
        json={
            "username": "mounir",
            "email": "mounir@example.com",
            "password": "StrongPass123!",
        },
    )

    assert response.status_code == 201
    assert response.get_json()["message"] == "User created successfully"


def test_register_duplicate_email(client):
    payload = {
        "username": "mounir",
        "email": "mounir@example.com",
        "password": "StrongPass123!",
    }

    assert client.post("/register", json=payload).status_code == 201
    response = client.post(
        "/register",
        json={
            "username": "another",
            "email": "mounir@example.com",
            "password": "StrongPass123!",
        },
    )

    assert response.status_code == 400
    assert response.get_json()["message"] == "User already exists"


def test_login_success(client):
    client.post(
        "/register",
        json={
            "username": "mounir",
            "email": "mounir@example.com",
            "password": "StrongPass123!",
        },
    )

    response = client.post(
        "/login",
        json={"email": "mounir@example.com", "password": "StrongPass123!"},
    )

    data = response.get_json()
    assert response.status_code == 200
    assert data["message"] == "Login successful"
    assert data["access_token"]
    assert data["user"]["email"] == "mounir@example.com"


def test_login_invalid_password(client):
    client.post(
        "/register",
        json={
            "username": "mounir",
            "email": "mounir@example.com",
            "password": "StrongPass123!",
        },
    )

    response = client.post(
        "/login",
        json={"email": "mounir@example.com", "password": "wrong"},
    )

    assert response.status_code == 401
    assert response.get_json()["message"] == "Invalid email or password"


def test_me_requires_token(client):
    response = client.get("/api/users/me")

    assert response.status_code == 401


def test_me_with_token(client):
    client.post(
        "/register",
        json={
            "username": "mounir",
            "email": "mounir@example.com",
            "password": "StrongPass123!",
        },
    )

    login = client.post(
        "/login",
        json={"email": "mounir@example.com", "password": "StrongPass123!"},
    )
    token = login.get_json()["access_token"]

    response = client.get(
        "/api/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    data = response.get_json()
    assert response.status_code == 200
    assert data["username"] == "mounir"
    assert data["email"] == "mounir@example.com"
