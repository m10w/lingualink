import requests
from fuzzywuzzy import fuzz, process

# <TODO>: this should be modified later to be able to select the input language
WIKIPEDIA_API_URL = "https://en.wikipedia.org/w/api.php"

def get_wikipedia_translation(word, target_language):
    """
    Orchestrates the process of finding the best Wikipedia translation by first
    attempting an exact match, and if necessary, falling back to fuzzy matching.
    """
    # Attempt to get an exact match
    exact_translation = exact_match_titles(word, target_language)

    if exact_translation:
        return {"suggestion": None, "translation": exact_translation}

    # If no exact match is found, attempt fuzzy matching
    fuzzy_result = fuzzy_match_titles(word, target_language)

    if fuzzy_result["translation"]:
        return {"suggestion": fuzzy_result["suggestion"], "translation": fuzzy_result["translation"]}

    return {"suggestion": None, "translation": "No Wikipedia translation available"}


def exact_match_titles(word, target_language):
    """
    Attempts to find an exact Wikipedia translation for the given word in the target language.
    """
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
        if langlinks:
            return langlinks[0]['*'] # Return the translated title in the target language
    return None

def fuzzy_match_titles(word, target_language):
    """
    Attempts to find a partial match for the word using fuzzy matching and checks
    if the best match has a valid translation in the target language.
    """
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

        # Validate that the best match has a translation in the target language
        translation = exact_match_titles(best_match, target_language)
        if translation and score > 0:
            return {"suggestion": f'{best_match} {score}', "translation": translation}

    return {"suggestion": None, "translation": None}