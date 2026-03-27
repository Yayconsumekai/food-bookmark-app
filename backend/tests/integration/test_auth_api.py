import pytest

class TestRegister:
    def test_register_success(self, client):
        response = client.post("/api/auth/register", json={
            "username": "newuser",
            "email":    "newuser@example.com",
            "password": "securepass123",
        })
        assert response.status_code == 201
        data = response.json()
        assert data["username"] == "newuser"
        assert data["email"]    == "newuser@example.com"
        assert "password" not in data   # never expose password

    def test_register_duplicate_email_fails(self, client, test_user):
        response = client.post("/api/auth/register", json={
            "username": "anotheruser",
            "email":    "test@example.com",   # already exists
            "password": "password123",
        })
        assert response.status_code == 400
        assert "Email" in response.json()["detail"]

    def test_register_duplicate_username_fails(self, client, test_user):
        response = client.post("/api/auth/register", json={
            "username": "testuser",            # already exists
            "email":    "unique@example.com",
            "password": "password123",
        })
        assert response.status_code == 400
        assert "Username" in response.json()["detail"]

    def test_register_missing_fields_fails(self, client):
        response = client.post("/api/auth/register", json={
            "username": "incomplete",
        })
        assert response.status_code == 422   # FastAPI validation error


class TestLogin:
    def test_login_success_returns_token(self, client, test_user):
        response = client.post("/api/auth/login", json={
            "email":    "test@example.com",
            "password": "password123",
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["user"]["email"] == "test@example.com"

    def test_login_wrong_password_fails(self, client, test_user):
        response = client.post("/api/auth/login", json={
            "email":    "test@example.com",
            "password": "wrongpassword",
        })
        assert response.status_code == 401

    def test_login_nonexistent_email_fails(self, client):
        response = client.post("/api/auth/login", json={
            "email":    "nobody@example.com",
            "password": "password123",
        })
        assert response.status_code == 401


class TestMe:
    def test_me_returns_current_user(self, client, auth_headers, test_user):
        response = client.get("/api/auth/me", headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["email"] == "test@example.com"

    def test_me_without_token_fails(self, client):
        response = client.get("/api/auth/me")
        assert response.status_code == 401

    def test_me_with_invalid_token_fails(self, client):
        response = client.get(
            "/api/auth/me",
            headers={"Authorization": "Bearer invalidtoken123"}
        )
        assert response.status_code == 401