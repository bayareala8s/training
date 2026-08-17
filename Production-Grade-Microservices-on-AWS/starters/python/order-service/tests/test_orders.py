from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    assert client.get("/health").json()["service"] == "order-service"


@patch("app.main.fetch_product")
@patch("app.main.publish_event")
def test_create_order(mock_publish, mock_fetch):
    mock_fetch.return_value = {
        "id": "prod-1",
        "name": "Test Product",
        "price": 10.0,
        "stock": 5,
    }
    response = client.post(
        "/orders",
        json={"user_id": "user-1", "items": [{"product_id": "prod-1", "quantity": 1}]},
    )
    assert response.status_code == 201
    mock_publish.assert_called_once()
