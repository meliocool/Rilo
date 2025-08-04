import speech_recognition as sr
import requests
import json
import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import stream

load_dotenv()

MODEL_NAME = "rilo"
OLLAMA_API_URL = "http://localhost:11434/api/generate"
TEMP_AUDIO_FILE = "temp_rilo_speech.mp3"

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

ELEVENLABS_VOICE_ID = "cgSgspJ2msm6clMCkdW9" 

try:
    if not ELEVENLABS_API_KEY:
        raise ValueError("ElevenLabs API key is not found. Please make sure it is set in your .env file.")
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
except Exception as e:
    print(f"FATAL: Could not initialize ElevenLabs client. {e}")
    exit()

def speak(text):
    print(f"Rilo: {text}")
    try:
        audio_stream = client.text_to_speech.stream(
            text=text,
            voice_id=ELEVENLABS_VOICE_ID,
            model_id="eleven_multilingual_v2"
        )
        stream(audio_stream)
    except Exception as e:
        print(f"Error communicating with ElevenLabs API: {e}")
    finally:
        if os.path.exists(TEMP_AUDIO_FILE):
            os.remove(TEMP_AUDIO_FILE)

def listen_for_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("\nListening...")
        recognizer.energy_threshold = 300 
        recognizer.pause_threshold = 1.5
        try:
            audio = recognizer.listen(source, timeout=8, phrase_time_limit=15)
        except sr.WaitTimeoutError:
            print("Listening timed out. Please try again.")
            return None

    try:
        print("Recognizing...")
        command = recognizer.recognize_google(audio)
        print(f"Dhitan said: {command}")
        return command
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand what you said. Please try again.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return None
    except Exception as e:
        print(f"An error occurred during speech recognition: {e}")
        return None

def ask_rilo(prompt):
    print("Rilo is thinking...")
    try:
        payload = {
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        }
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=60)
        response.raise_for_status()
        response_data = response.json()
        return response_data.get('response', 'Sorry, I could not get a response.').strip()

    except requests.exceptions.RequestException as e:
        return f"Error connecting to Ollama: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

def main():
    speak("What's up! Rilo is online with a voice, How can i help today?")
    
    while True:
        user_prompt = listen_for_command()
        if user_prompt:
            if "goodbye rilo" in user_prompt.lower():
                speak("Alright, catch you later!")
                break
            
            rilo_response = ask_rilo(user_prompt)
            speak(rilo_response)

if __name__ == "__main__":
    main()
