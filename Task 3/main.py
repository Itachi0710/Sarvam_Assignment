from fastapi import FastAPI
from pydantic import BaseModel
import requests
from datetime import datetime
import os

app = FastAPI()

# Sarvam Text-to-Speech API endpoint
SARVAM_TTS_API_URL = "https://api.sarvam.ai/text-to-speech"
# key generated form website for test
SARVAM_TTS_API_KEY = "02c6352c-3ae3-44cc-ae31-5fd546b7b7cb"

class Agent:
    def __init__(self):
        pass

    def decide_action(self, query: str):
        vectordb_keywords = ["information", "search", "lookup", "find"]

        if query.lower() in ["hello", "hi", "hey"]:
            return "greet"
        elif any(keyword in query.lower() for keyword in vectordb_keywords):
            return "vectordb"
        elif "time" in query.lower():
            return "time"
        elif "translate" in query.lower():
            return "translate"
        else:
            return "unknown"

    def perform_action(self, action: str, query: str):
        if action == "greet":
            return "Hello! How can I assist you today?"
        elif action == "vectordb":
            return "Fetching information from VectorDB..."
        elif action == "time":
            return f"The current time is {datetime.now().strftime('%H:%M:%S')}"
        elif action == "translate":
            return self.translate_text(query)
        else:
            return "I'm not sure how to help with that."

    def generate_audio(self, text: str):
        headers = {
            'Content-Type': 'application/json',
            'api-subscription-key': SARVAM_TTS_API_KEY
        }
        data = {
            "inputs": [text],
            "target_language_code": "hi-IN",
            "speaker": "meera",
            "pitch": 0,
            "pace": 1.65,
            "loudness": 1.5,
            "speech_sample_rate": 8000,
            "enable_preprocessing": True,
            "model": "bulbul:v1"
        }
        response = requests.post(SARVAM_TTS_API_URL, headers=headers, json=data)

        if response.status_code == 200:
            audio_file_path = "output.wav"
            with open(audio_file_path, "wb") as out:
                out.write(response.content)
            return audio_file_path
        else:
            return "Error generating voice"

    def translate_text(self, text: str):
        return "Translation feature not implemented."

class QueryRequest(BaseModel):
    query: str

agent = Agent()

@app.post("/agent")
async def handle_agent(request: QueryRequest):
    query = request.query
    action = agent.decide_action(query)
    response_text = agent.perform_action(action, query)
    audio_file = agent.generate_audio(response_text) if action != "translate" else None
    return {"response": response_text, "audio_file": audio_file}
