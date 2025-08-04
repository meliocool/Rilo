import os
from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = "rilo"
OLLAMA_API_URL = "http://localhost:11434/api/generate"

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_VOICE_ID = os.getenv("VOICE_ID")

SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")

MIC_ENERGY_THRESHOLD = 300
MIC_PAUSE_THRESHOLD = 1.5
WAKE_WORD = "hey rilo"