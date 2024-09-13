from flask import Flask, render_template, request, jsonify
from lingualink.models.translation import translate_text
from utils.wikipedia import get_wikipedia_translation
import logging

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Translation route (uses the translation model logic)
@app.route('/translate', methods=['POST'])
def translate():
    data = request.json
    word = data.get('word')
    language = data.get('language')
    logging.info(f"Received word: {word} for language: {language}")

    if not word or not language:
        return jsonify({'error': 'Invalid input, please provide a word and a language.'}), 400
    # Use the translation model to translate the word
    try:
        # Get Wikipedia translation
        wikipedia_translation = get_wikipedia_translation(word, language)

        # Get machine translation
        machine_translation = translate_text(word, language)

        return jsonify({
            'wikipedia_translation': wikipedia_translation or 'No Wikipedia translation available',
            'machine_translation': machine_translation
        })
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
