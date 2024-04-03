from flask import Flask, render_template, jsonify, request
from os import getenv
from dotenv import load_dotenv
import requests
from record import speech_to_text
import openai
import elevenlabs

app = Flask(__name__)

# Load API keys from environment variables
load_dotenv()
OPENAI_API_KEY = getenv("OPENAI_API_KEY", "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")
DEEPGRAM_API_KEY = getenv("DEEPGRAM_API_KEY", "b80d994415427ffa3879788b4820fc50a90404a8")
ELEVENLABS_API_KEY = getenv("ELEVENLABS_API_KEY", "913fb99a2b593650ba5951d5e24b4243")

# Initialize APIs with the keys
gpt_client = openai.Client(api_key=OPENAI_API_KEY)
elevenlabs.set_api_key(ELEVENLABS_API_KEY)

context = "You are Jarvis, Alex's human assistant..."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/record', methods=['POST'])
def record_audio():
    speech_to_text()  # Call the function from record.py
    return jsonify({'success': True})

@app.route('/conversation')
def get_conversation():
    with open('conv.txt', 'r') as f:
        conversation = f.readlines()
    return jsonify({'conversation': conversation})

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    audio_file = request.files['audio']
    audio_data = audio_file.read()

    deepgram_url = 'https://api.deepgram.com/v1/listen'
    headers = {
        'Authorization': f'Token {DEEPGRAM_API_KEY}',
        'Content-Type': 'audio/wav',  # Adjust content type based on your audio format
    }

    response = requests.post(deepgram_url, headers=headers, data=audio_data)

    if response.status_code == 200:
        transcription = response.json().get('transcripts')[0]['text']
        return jsonify({'transcription': transcription})
    else:
        return jsonify({'error': f"Error: {response.status_code} - {response.text}"}), 500

if __name__ == '__main__':
    app.run(debug=True)

