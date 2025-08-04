import requests
import json
import config

def ask_rilo_for_json(prompt):
    system_prompt = f"""
    You are an intent recognition engine. Analyze the user's request and provide a JSON object describing the action.
    The possible actions are 'play_song_on_spotify'.
    If the action is 'play_song_on_spotify', you must extract the 'song_name' and the 'artist'.
    If you cannot determine the song or artist, return an empty JSON object.
    Do not add any explanation, only return the JSON object.

    User request: "{prompt}"

    JSON response:
    """
    print("Rilo is interpreting the command...")
    try:
        payload = {"model": config.MODEL_NAME, "prompt": system_prompt, "stream": False, "format": "json"}
        response = requests.post(config.OLLAMA_API_URL, json=payload, timeout=60)
        response.raise_for_status()
        response_data = response.json()
        return json.loads(response_data.get('response', '{}'))
    except Exception as e:
        print(f"Error getting structured command from Rilo: {e}")
        return {}

def ask_rilo_for_chat(prompt):
    print("Rilo is thinking...")
    try:
        payload = {"model": config.MODEL_NAME, "prompt": prompt, "stream": False}
        response = requests.post(config.OLLAMA_API_URL, json=payload, timeout=60)
        response.raise_for_status()
        response_data = response.json()
        return response_data.get('response', 'Sorry, I could not get a response.').strip()
    except Exception as e:
        return f"Error connecting to Ollama: {e}"