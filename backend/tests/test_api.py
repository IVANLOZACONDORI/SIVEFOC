from fastapi.testclient import TestClient
from app.main import app

def test_health():
    response = TestClient(app).get('/health')
    assert response.status_code == 200
    assert response.json()['status'] == 'ok'

def test_protected_endpoints_reject_anonymous():
    client = TestClient(app)
    assert client.get('/v1/me').status_code == 401
    assert client.get('/v1/institutions').status_code == 401
    assert client.get('/v1/competencies', headers={'X-Institution-Id':'fake'}).status_code == 401
