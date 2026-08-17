from fastapi.testclient import TestClient

from app.main import app


def test_health():
    with TestClient(app) as client:
        assert client.get("/health").status_code == 200


def test_list_seeded_products():
    with TestClient(app) as client:
        response = client.get("/products")
        assert response.status_code == 200
        assert len(response.json()) >= 1
