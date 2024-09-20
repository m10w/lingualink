from flask import Flask, render_template, request, jsonify
from lingualink.models.translation import translate_text
from .utils.wikipedia import get_wikipedia_translation
import logging
from .supported_languages import supported_languages

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)


# Home route
@app.route('/')
def index():
    return render_template('index.html', languages=supported_languages)


# Translation route (uses the translation model logic)
@app.route('/translate', methods=['POST'])
def translate():
    data = request.json
    word = data.get('word')
    language = data.get('language')
    logging.info(f"Received word: {word} for language: {language}")

    if not word or not language or language not in supported_languages:
        return jsonify({'error': 'Invalid input, please provide a word and a valid language.'}), 400

    wikipedia_translation = None
    machine_translation = None

    # check if the selected language is supported by wikipedia
    if supported_languages[language]['wikipedia']:
        wikipedia_translation = get_wikipedia_translation(word, language)

    # check if the selected language is supported by machine translation
    if supported_languages[language]['machine']:
        machine_translation = translate_text(word, language)

    return jsonify({
        'wikipedia_translation': wikipedia_translation or 'No Wikipedia translation available',
        'machine_translation': machine_translation or 'No Machine translation available'
    })

if __name__ == '__main__':
    app.run(debug=True)
