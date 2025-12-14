from fastapi.testclient import TestClient
from app.main import app


def test_home_loads():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert "Clínica Veterinaria" in response.text
