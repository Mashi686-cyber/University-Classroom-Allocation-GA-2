from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_get_datasets():
    response = client.get("/api/datasets")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    
def test_get_config():
    response = client.get("/api/config")
    assert response.status_code == 200
    assert "population_size" in response.json()

def test_get_experiments():
    response = client.get("/api/experiments")
    assert response.status_code == 200
