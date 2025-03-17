import pytest
from ..main import create_integrated_app

@pytest.fixture
def app():
    app = create_integrated_app()
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_home_endpoint(client):
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'ok'
    assert 'endpoints' in data
    assert len(data['endpoints']) == 3

def test_endpoints_exist(client):
    endpoints = ['/disaster', '/ml', '/social']
    for endpoint in endpoints:
        response = client.get(endpoint)
        assert response.status_code != 404, f"Endpoint {endpoint} not found" 