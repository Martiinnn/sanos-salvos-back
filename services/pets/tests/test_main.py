from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200

def test_404():
    response = client.get("/ruta-invalida-para-probar-404")
    assert response.status_code == 404
