from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_analyze_returns_valid_structure():
    response = client.post("/analyze", json={"text": "I am so happy today!"})
    assert response.status_code == 200
    data = response.json()
    assert "character" in data
    assert "dominant_emotion" in data
    assert 0 <= data["confidence"] <= 1

def test_analyze_rejects_empty_text():
    response = client.post("/analyze", json={"text": ""})
    assert response.status_code == 422