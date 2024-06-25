from google_trans_new import google_translator
import requests
from dotenv import load_dotenv
import os
from flask import Flask, request, jsonify, Response
from flask_cors import CORS, cross_origin
import logging
import time

load_dotenv()
logging.basicConfig(level=logging.DEBUG)

translator = google_translator(timeout=10)

API_KEY = os.getenv('API_KEY')
ENDPOINT = "https://api.openai.com/v1/chat/completions"

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Access-Control-Allow-Origin'

def openai_request_with_retry(payload, headers, retries=3, timeout=60, backoff_factor=1):
    for attempt in range(retries):
        try:
            response = requests.post(ENDPOINT, json=payload, headers=headers, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt < retries - 1:
                sleep_time = backoff_factor * (2 ** attempt)
                logging.info(f"Retrying in {sleep_time} seconds...")
                time.sleep(sleep_time)
            else:
                raise

@app.route('/')
def index():
    return 'Welcome to the Translator API!'

@app.route('/translate', methods=['POST'])
@cross_origin()
def translate_and_improve():
    try:
        data = request.get_json()
        logging.debug(f"Received data: {data}")
        text = data.get("text")
        dest_lang = data.get("dest_lang")

        # if not text or not dest_lang:
        #     return jsonify({'error': 'Invalid input'}), 400

        # translation = translator.translate(text, lang_tgt=dest_lang)

        # translated_text = translation.text
        # logging.debug(f"Google translation result: {translation.text}")
        # improved_text = gpt_improve(translated_text)
        improved_text = gpt_improve(text, dest_lang)
        return jsonify({'translated_text': improved_text})
    except Exception as e:
        logging.error(f"Error during translation: {str(e)}")
        return jsonify({'error': str(e)}), 500

def gpt_improve(text, dest_lang, api_key=API_KEY, model="gpt-3.5-turbo", temperature=0.5, max_tokens=2048, stream=True):
    endpoint = ENDPOINT
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        # {"role": "user", "content": f"Make the following text sound more natural in its original language: {text}"}
        {"role": "user", "content": f"Translate the following text to {dest_lang}: {text}"}
    ]

    data = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": stream
    }

    response_data = openai_request_with_retry(data, headers)

    return response_data['choices'][0]['message']['content']

if __name__ == '__main__':
    app.run(debug=True)
