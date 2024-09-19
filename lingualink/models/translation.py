from ..supported_languages import supported_languages
from transformers import MarianMTModel, MarianTokenizer
from functools import lru_cache
import logging

logging.basicConfig(level=logging.INFO)

model_cache = {} # Cache for storing models
def preload_models():
    # Preload all models into cache at startup
    for language_code, lang_data in supported_languages.items():
        model_name = lang_data.get('model_name')
        if model_name:
            model = MarianMTModel.from_pretrained(model_name)
            tokenizer = MarianTokenizer.from_pretrained(model_name)
            model_cache[language_code] = (model, tokenizer)
            logging.info(f"Preloaded model for language: {language_code}.")

# Automatically preload all models.
preload_models()

# Function to load model and tokenizer
def load_model(language_code):
    if language_code in model_cache:
        return model_cache[language_code]
    else:
        raise ValueError(f"No model available for language code {language_code}")

# Function to perform the translation
@lru_cache(maxsize=100)
def translate_text(text, language_code):
    model, tokenizer = load_model(language_code)
    inputs = tokenizer.encode(text, return_tensors="pt", padding=True)
    translated = model.generate(inputs)
    translated_text = tokenizer.decode(translated[0], skip_special_tokens=True)
    return translated_text

