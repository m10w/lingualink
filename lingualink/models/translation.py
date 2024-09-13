from transformers import MarianMTModel, MarianTokenizer

# Dictionary to store the model name per language code
model_name_dict = {
    'de': 'Helsinki-NLP/opus-mt-en-de',  # English to German
    'fr': 'Helsinki-NLP/opus-mt-en-fr',  # English to French
    'es': 'Helsinki-NLP/opus-mt-en-es'   # English to Spanish
}

# Function to load model and tokenizer
def load_model(language_code):
    model_name = model_name_dict.get(language_code)
    if model_name:
        model = MarianMTModel.from_pretrained(model_name)
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        return model, tokenizer
    else:
        raise ValueError(f"No model available for language code {language_code}")

# Function to perform the translation
def translate_text(text, language_code):
    model, tokenizer = load_model(language_code)
    inputs = tokenizer.encode(text, return_tensors="pt", padding=True)
    translated = model.generate(inputs)
    translated_text = tokenizer.decode(translated[0], skip_special_tokens=True)
    return translated_text

