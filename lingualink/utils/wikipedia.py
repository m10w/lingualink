import requests

# <TODO>: this should be modified later to be able to select the input language
WIKIPEDIA_API_URL = "https://en.wikipedia.org/w/api.php"

def get_wikipedia_translation(word, target_language):
    params = {
        'action': 'query',
        'titles': word,
        'prop': 'langlinks',
        'lllang': target_language,
        'format': 'json'
    }
    response = requests.get(WIKIPEDIA_API_URL, params=params)
    data = response.json()

    pages = data.get('query', {}).get('pages', {})
    for page_id, page_data in pages.items():
        langlinks = page_data.get('langlinks', [])
        if langlinks:
            return langlinks[0]['*']  # Return the translated title in the target language

    return None  # If no translation is found
