from googletrans import Translator
import openai
import requests
import json
from dotenv import load_dotenv
import os


load_dotenv()

API_KEY = os.getenv('OPENAI_API_KEY')
ENDPOINT = "https://api.openai.com/v1/chat/completions"


def ggl_translate(text, dest_lang):
  translator = Translator()
  translation = translator.translate(text, dest=dest_lang)
  return translation.text

def gpt_improve(text, api_key, model, messages, temperature=0.5, max_tokens=2048)
    endpoint = ENDPOINT
    api_key = API_KEY
    text = ggl_translate(text)
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    
    data = {
      "model": "gpt-3.5-turbo",
      "messages": [{"role": "system", "content": "You are a helpful assistant."},
                   {"role": "user", "content": "make the following text sound more natural in its original language:" text}
                  ]
      "temperature": 0.5,
      "max_tokens": 2048
    }
    
    response = requests.post(endpoint, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        response_data = response.json()
        return jsonify({response_data['choices'][0]['message']['content'].text)
    else:
        return jsonify("Error: "response.status_code", " response.text)


if __name__ == '__main__':
    app.run(debug=True)
