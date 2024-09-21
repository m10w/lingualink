import pytest
from lingualink.models.translation import translate_text


def test_translation_english_to_german():
    # Test translation of a word from English to German
    result = translate_text("hello", "de")
    assert "Guten Tag" in result


def test_translation_english_to_french():
    # Test translation of a word from English to French
    result = translate_text("hello", "fr")
    assert "Bonjour" in result


def test_invalid_language_code():
    # Test translation with an invalid language code
    with pytest.raises(ValueError):
        translate_text("hello", "xyz")
