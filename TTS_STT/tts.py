import config
from elevenlabs.client import ElevenLabs
from elevenlabs import stream

try:
    if not config.ELEVENLABS_API_KEY:
        raise ValueError("ElevenLabs API key is not found in .env file.")
    
    client = ElevenLabs(api_key=config.ELEVENLABS_API_KEY)

except Exception as e:
    print(f"FATAL: Could not initialize ElevenLabs client. {e}")
    client = None

def speak(text):
    if not client:
        print("ElevenLabs client not initialized. Cannot speak.")
        return

    print(f"Rilo: {text}")
    try:
        audio_stream = client.text_to_speech.stream(
            text=text, 
            voice_id=config.ELEVENLABS_VOICE_ID, 
            model_id="eleven_multilingual_v2"
        )
        stream(audio_stream)
    except Exception as e:
        print(f"Error communicating with ElevenLabs API: {e}")