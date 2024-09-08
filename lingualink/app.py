from flask import Flask, request, jsonify, render_template
from transformers import MarianMTModel, MarianTokenizer
from langchain import OpenAI, LangChain
from langchain.chains import SimpleChain

app = Flask(__name__)

# Initialize LangChain with OpenAI API (Replace 'YOUR_OPENAI_API_KEY' with your actual API key)
llm = OpenAI(api_key="")
langchain = LangChain(llm)

model_name_dict = {
    'de': 'Helsinki-NLP/opus-mt-en-de',
    'fr': 'Helsinki-NLP/opus-mt-en-fr',
    'es': 'Helsinki-NLP/opus-mt-en-es'
    # Add more languages as needed
}

class TranslationChain(SimpleChain):
    def __init__(self, input_text, target_language):
        self.input_text = input_text
        self.target_language = target_language

    def _call(self):
        prompt_template = f"Translate the following text to {self.target_language}: {self.input_text}"
        response = langchain.llm(prompt_template)
        return response

def translate_text_with_langchain(text, language):
    model_name = model_name_dict.get(language, 'Helsinki-NLP/opus-mt-en-de')
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)
    inputs = tokenizer.encode(text, return_tensors="pt", padding=True)
    translated = model.generate(inputs)
    translated_text = tokenizer.decode(translated[0], skip_special_tokens=True)

    # Integrate LangChain for improved translation
    translation_chain = TranslationChain(translated_text, language)
    improved_translation = translation_chain.run()
    return improved_translation

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    data = request.json
    word = data['word']
    language = data['language']
    translation = translate_text_with_langchain(word, language)
    return jsonify({'translation': translation})

if __name__ == '__main__':
    app.run(debug=True)
