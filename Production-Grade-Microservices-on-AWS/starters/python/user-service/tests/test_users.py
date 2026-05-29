import time

from fastapi.testclient import TestClient

from app.main import app


def test_health():
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["service"] == "user-service"


def test_create_and_login_user():
    email = f"test-{int(time.time())}@example.com"
    with TestClient(app) as client:
        client.post(
            "/users",
            json={"email": email, "name": "Test User", "password": "password123"},
        )
        login = client.post(
            "/auth/login", json={"email": email, "password": "password123"}
        )
        assert login.status_code == 200
        assert "access_token" in login.json()
