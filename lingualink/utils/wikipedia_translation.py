import requests
from fuzzywuzzy import fuzz, process

# <TODO>: this should be modified later to be able to select the input language
WIKIPEDIA_API_URL = "https://en.wikipedia.org/w/api.php"

def get_wikipedia_translation(word, target_language):
    """
    Orchestrates the process of finding the best Wikipedia translation by first
    attempting an exact match, and if necessary, falling back to fuzzy matching.
    If a disambiguation page is found, gathers possible meanings from the
    disambiguation page.
    """

    # Initialize the result structure
    result = {"translation": None, "suggestion": None}

    # Attempt to get an exact match
    exact_translation = exact_match_titles(word, target_language)

    if exact_translation["translation"]:
        result = exact_translation
        return result

    # If no exact match is found, attempt fuzzy matching
    fuzzy_result = fuzzy_match_titles(word, target_language)

    if fuzzy_result["translation"]:
        result["suggestion"] = fuzzy_result["suggestion"]
        result["translation"]=  fuzzy_result["translation"]
        return result

    # If both exact and fuzzy matching fail, fall back to searching for disambiguation entries
    disambiguation_suggestion = search_wikipedia(word, target_language)
    if disambiguation_suggestion:
        result["suggestion"] = disambiguation_suggestion # No translation, but provide suggestions

    return result


def exact_match_titles(word, target_language):
    """
    Attempts to find an exact Wikipedia translation for the given word in the target language.
    Checks for disambiguation pages and handles accordingly.
    """
    params = {
        "action": "query",
        "titles": word,
        "prop": "langlinks|categories", # Check for categories, useful for disambiguations
        "lllang": target_language,
        "format": "json",
    }
    response = requests.get(WIKIPEDIA_API_URL, params=params)
    data = response.json()

    pages = data.get("query", {}).get("pages", {})
    langlinks = None
    for page_id, page_data in pages.items():
        if 'disambiguation' in page_data.get('categories', []):
            # Disambiguation page detected, return suggestion
            return {"translation": None, "suggestion": search_wikipedia(word, target_language)}

        langlinks = page_data.get("langlinks", [])
        if langlinks:
            return {"translation": langlinks[0]['*'], "suggestion": None}

    return {"translation": None, "suggestion": None}

def fuzzy_match_titles(word, target_language):
    """
    Attempts to find a partial match for the word using fuzzy matching and checks
    if the best match has a valid translation in the target language. Also handles
    disambiguation detection.
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
        translation_result = exact_match_titles(best_match, target_language)
        if translation_result["translation"] and score > 0:
            return {"suggestion": f'{best_match} ({score}%)', "translation": translation_result["translation"]}

        if translation_result["suggestion"]:
            return {"suggestion": translation_result["suggestion"], "translation": None}

    return {"suggestion": None, "translation": None}


def search_wikipedia(word, target_language):
    """
    Search Wikipedia for multiple meanings of an ambiguous word in the target language.
    Retrieves disambiguation pages or relevant entries.
    """
    search_params = {
        'action': 'query',
        'list': 'search',
        'srsearch': word,
        'format': 'json',
        'srlimit': 5,  # Limit to 5 search results for disambiguation
        'srprop': 'snippet',  # Get a snippet to display a preview of the article
        'srwhat': 'text',  # Search the content of articles, not just titles
    }

    search_response = requests.get(f'https://{target_language}.wikipedia.org/w/api.php', params=search_params)
    search_data = search_response.json()

    # Extract titles and snippets from search results for disambiguation
    suggestions = [{"title": result['title'],
                    "snippet": result['snippet']}
                   for result in search_data.get('query', {}).get('search', [])]

    return suggestions