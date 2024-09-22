import pytest
import requests
from unittest.mock import patch
from lingualink.utils.wikipedia_translation import get_wikipedia_translation

WIKIPEDIA_API_URL = "https://en.wikipedia.org/w/api.php"


# Test case 1: Successful translation
@patch("lingualink.utils.wikipedia_translation.requests.get")
def test_get_wikipedia_translation_success(mock_get):
    # Mocking the response data to simulate a successful translation
    mock_response = {
        "query": {
            "pages": {
                "12345": {
                    "langlinks": [{"*": "Hallo"}]  # Example translation in German
                }
            }
        }
    }
    mock_get.return_value.json.return_value = mock_response

    result = get_wikipedia_translation("Hello", "de")
    assert result == "Hallo"


# Test case 2: No translation found
@patch("lingualink.utils.wikipedia_translation.requests.get")
def test_get_wikipedia_translation_no_translation(mock_get):
    # Mocking a response with no translation (empty langlinks)

    mock_response = {
        "query": {"pages": {"12345": {"langlinks": []}}}  # No translation available
    }
    mock_get.return_value.json.return_value = mock_response

    result = get_wikipedia_translation("Hello", "de")
    assert result is None


# Test case 3: Wikipedia page not found
@patch("lingualink.utils.wikipedia_translation.requests.get")
def test_get_wikipedia_translation_page_not_found(mock_get):
    # Mocking a response with no valid pages
    mock_response = {"query": {"pages": {}}}
    mock_get.return_value.json.return_value = mock_response

    result = get_wikipedia_translation("NonExistentWord", "de")
    assert result is None


# Test case 4: API request failure
@patch("lingualink.utils.wikipedia_translation.requests.get")
def test_get_wikipedia_translation_api_failure(mock_get):
    # Mocking an exception to simulate a network failure
    mock_get.side_effect = requests.exceptions.RequestException

    with pytest.raises(requests.exceptions.RequestException):
        get_wikipedia_translation("Hello", "de")
