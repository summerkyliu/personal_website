from google.cloud import translate_v2 as translate
import requests
import json
from dotenv import load_dotenv
import os
from flask import Flask, request, jsonify

load_dotenv()

translate_client = translate.Client()

API_KEY = os.getenv('API_KEY')
ENDPOINT = "https://api.openai.com/v1/chat/completions"

app = Flask(__name__)

@app.route('/translate', methods=['POST'])
def translate_and_improve():
    data = request.get_json()
    text = data.get("text")
    dest_lang = data.get("dest_lang")
    
    if not text or not dest_lang:
        return jsonify({'error': 'Invalid input'}), 400
    
    translation = translate_client.translate(text, target_language=dest_lang)
    translated_text = translation['translatedText']
    
    improved_text = gpt_improve(translated_text)
    
    return jsonify({'translated_text': improved_text})


def gpt_improve(text, api_key=API_KEY, model="gpt-3.5-turbo", temperature=0.5, max_tokens=2048):
    endpoint = ENDPOINT
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"Make the following text sound more natural in its original language: {text}"}
    ]
    
    data = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    
    response = requests.post(endpoint, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        response_data = response.json()
        return response_data['choices'][0]['message']['content']
    else:
        return f"Error: {response.status_code}, {response.text}"



if __name__ == '__main__':
    app.run(debug=True)
