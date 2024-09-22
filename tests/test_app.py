import pytest
from lingualink.app import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_home_page(client):
    """Test if the home page loads correctly"""
    response = client.get("/")
    assert response.status_code == 200
    assert b"LinguaLink Translator" in response.data


def test_translation_route(client):
    """Test the /translate route"""
    response = client.post("/translate", json={"word": "hello", "language": "de"})
    assert response.status_code == 200
    assert b"Guten Tag" in response.data

def test_invalid_inputs(client):
    """Test the behavior with invalid inputs"""
    response = client.post("/translate", json={"word": "", "language": ""})
    assert response.status_code == 400
    assert b"error" in response.data
