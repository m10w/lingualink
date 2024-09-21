import pytest
from lingualink.app import app  # Import the Flask app from your main app file

@pytest.fixture
def client():
    # This sets up the Flask test client
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# Smoke test to check if the app starts up and /translate endpoint works
@pytest.mark.critical
def test_smoke(client):
    # Send a POST request to the /translate endpoint
    response = client.post('/translate', json={'word': 'Hello', 'language': 'de'})

    # Check if the status code is 200 (success)
    assert response.status_code == 200

    # Optionally, check if the response contains the expected keys
    data = response.get_json()
    assert 'machine_translation' in data  # Ensures that 'translation' is in the response
    assert 'wikipedia_translation' in data  # Ensures that 'translation' is in the response
