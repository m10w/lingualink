import requests
from fuzzywuzzy import fuzz, process

# <TODO>: this should be modified later to be able to select the input language
WIKIPEDIA_API_URL = "https://en.wikipedia.org/w/api.php"


def get_wikipedia_translation(word, target_language):
    params = {
        "action": "query",
        "titles": word,
        "prop": "langlinks",
        "lllang": target_language,
        "format": "json",
    }
    response = requests.get(WIKIPEDIA_API_URL, params=params)
    data = response.json()

    pages = data.get("query", {}).get("pages", {})
    langlinks = None
    for page_id, page_data in pages.items():
        langlinks = page_data.get("langlinks", [])

    # If no exact match found, use fuzzy matching
    if not langlinks:
        return fuzzy_match_titles(word, target_language)

    return langlinks[0]['*'] if langlinks else None

def fuzzy_match_titles(word, target_language):
    # Query wikipedia for possible matches (e.g., list all pages in the target language
    search_params = {
        'action': 'query',
        'list': 'search',
        'srsearch': word,
        'format': 'json',
    }
    search_response = requests.get(WIKIPEDIA_API_URL, params=search_params)
    search_data = search_response.json()

    # Get titles from seach results
    titles =[result['title'] for result in search_data.get('query', {}).get('search', [])]

    if titles:
        # Use fuzzy matching to find the best match
        best_match, score = process.extractOne(word, titles, scorer=fuzz.ratio)

        # If the score is good enough, return the best match
        if score > 50:
            return f"Did you mean: {best_match}?"

    return None