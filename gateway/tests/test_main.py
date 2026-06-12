from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "service": "api-gateway",
        "version": "1.0.0",
    }

def test_cors_headers():
    response = client.options("/health", headers={
        "Origin": "http://localhost:3000",
        "Access-Control-Request-Method": "GET"
    })
    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers

def test_invalid_route():
    response = client.get("/api/not-a-valid-route")
    assert response.status_code == 404

def test_unauthorized_post_report():
    response = client.post("/api/pets/reports", json={})
    assert response.status_code == 401
