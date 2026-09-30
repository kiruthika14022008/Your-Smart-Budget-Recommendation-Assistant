import os

os.environ[
    "USE_MOCK_RECOMMENDATIONS"
] = "true"


from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health():

    response = client.get(
        "/health"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"


def test_register_and_login():

    email = (
        "test_user_pocketsmart@example.com"
    )

    register_response = client.post(
        "/api/register",
        json={
            "name": "Test User",
            "email": email,
            "password": "secret123",
        },
    )

    assert register_response.status_code in {
        200,
        400,
    }


    login_response = client.post(
        "/api/login",
        json={
            "email": email,
            "password": "secret123",
        },
    )

    assert login_response.status_code == 200

    data = login_response.json()

    assert "access_token" in data