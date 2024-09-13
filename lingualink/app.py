from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Translation route (this will be connected to the ML model later)
@app.route('/translate', methods=['POST'])
def translate():
    data = request.json
    word = data.get('word')
    language = data.get('language')

    # Placeholder logic for now (will be replaced with ML model logic)
    translated_word = f"{word} translated to {language}"

    return jsonify({'translation': translated_word})

if __name__ == '__main__':
    app.run(debug=True)