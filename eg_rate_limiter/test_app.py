# test_app.py
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to the rate-limited API!" in response.data

def test_limited_endpoint(client):
    # Test that the endpoint works
    response = client.get('/limited')
    assert response.status_code == 200
    assert b"This endpoint is rate-limited to 5 requests per minute." in response.data

    # Test rate limiting
    for _ in range(5):
        response = client.get('/limited')
        assert response.status_code == 200

    # This should be rate limited
    response = client.get('/limited')
    assert response.status_code == 429