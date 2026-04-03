"""
Tests for authentication – register, login, duplicate handling, invalid creds.
"""

from tests.conftest import auth_header


class TestRegistration:
    def test_register_success(self, client):
        resp = client.post("/api/auth/register", json={
            "username": "newuser",
            "email": "new@test.com",
            "password": "Secure@1",
        })
        assert resp.status_code == 201
        data = resp.json()
        assert data["username"] == "newuser"
        assert data["role"] == "viewer"

    def test_register_duplicate_username(self, client, admin_user):
        resp = client.post("/api/auth/register", json={
            "username": "admin",
            "email": "other@test.com",
            "password": "Secure@1",
        })
        assert resp.status_code == 409

    def test_register_duplicate_email(self, client, admin_user):
        resp = client.post("/api/auth/register", json={
            "username": "other",
            "email": "admin@test.com",
            "password": "Secure@1",
        })
        assert resp.status_code == 409

    def test_register_short_password(self, client):
        resp = client.post("/api/auth/register", json={
            "username": "shortpw",
            "email": "short@test.com",
            "password": "123",
        })
        assert resp.status_code == 422

    def test_register_invalid_email(self, client):
        resp = client.post("/api/auth/register", json={
            "username": "bademail",
            "email": "not-an-email",
            "password": "Secure@1",
        })
        assert resp.status_code == 422


class TestLogin:
    def test_login_success(self, client, admin_user):
        resp = client.post("/api/auth/login", data={
            "username": "admin",
            "password": "Test@123",
        })
        assert resp.status_code == 200
        assert "access_token" in resp.json()

    def test_login_wrong_password(self, client, admin_user):
        resp = client.post("/api/auth/login", data={
            "username": "admin",
            "password": "WrongPass",
        })
        assert resp.status_code == 401

    def test_login_nonexistent_user(self, client):
        resp = client.post("/api/auth/login", data={
            "username": "ghost",
            "password": "Test@123",
        })
        assert resp.status_code == 401
