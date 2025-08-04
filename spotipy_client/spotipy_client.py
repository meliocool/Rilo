import spotipy
from spotipy.oauth2 import SpotifyOAuth
import config
from TTS_STT import tts

"""FULLY VIBE CODED WITH GEMINI (i didnt know a python package called spotipy even existed before this lmao)"""

try:
    if not all([config.SPOTIPY_CLIENT_ID, config.SPOTIPY_CLIENT_SECRET, config.SPOTIPY_REDIRECT_URI]):
        raise ValueError("Spotify credentials not found in .env file.")
    
    scope = "user-modify-playback-state user-read-playback-state"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    
    spotify_user_id = sp.current_user()['id']

except Exception as e:
    print(f"FATAL: Could not initialize Spotify client. {e}")
    sp = None

def execute_spotify_command(command_data):
    if not sp:
        print("Spotify client not initialized. Cannot execute command.")
        tts.speak("My connection to Spotify isn't working right now. Please check the setup.")
        return

    action = command_data.get("action")
    if action == "play_song_on_spotify":
        song_name = command_data.get("song_name")
        artist = command_data.get("artist")
        if not song_name or not artist:
            tts.speak("Sorry, I couldn't figure out the exact song or artist. Can you be more specific?")
            return

        tts.speak(f"Alright, searching for {song_name} by {artist} on Spotify.")
        try:
            query = f"track:{song_name} artist:{artist}"
            results = sp.search(q=query, type='track', limit=1)
            
            tracks = results['tracks']['items']
            if not tracks:
                tts.speak("I couldn't find that song. Maybe try another one?")
                return
            
            track_uri = tracks[0]['uri']
            devices = sp.devices()
            if not devices or not devices['devices']:
                tts.speak("I can't find an active Spotify device. Please open Spotify on your computer or phone and try again.")
                return

            device_id = devices['devices'][0]['id']

            sp.start_playback(device_id=device_id, uris=[track_uri])
            tts.speak(f"Now playing {song_name} by {artist}.")
            
        except Exception as e:
            tts.speak("I ran into an issue trying to play the song on Spotify.")
            print(f"Spotify error: {e}")