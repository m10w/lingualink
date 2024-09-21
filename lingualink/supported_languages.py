# supported_languages.py

# Dictionary that defines languages and which method supports them
supported_languages = {
    "de": {
        "name": "German",
        "wikipedia": True,
        "machine": True,
        "model_name": "Helsinki-NLP/opus-mt-en-de",
    },
    "fr": {
        "name": "French",
        "wikipedia": True,
        "machine": True,
        "model_name": "Helsinki-NLP/opus-mt-en-fr",
    },
    "nl": {
        "name": "Dutch",
        "wikipedia": True,
        "machine": True,
        "model_name": "Helsinki-NLP/opus-mt-en-nl",
    },
    "fa": {"name": "Farsi", "wikipedia": True, "machine": False, "model_name": None},
    "es": {"name": "Spanish", "wikipedia": True, "machine": False, "model_name": None},
}
