from TTS_STT import tts, stt
from llm import llm
from spotipy_client import spotipy_client
import time

def main():
    stop_listening = stt.start_background_listening()
    tts.speak("What's up! Rilo is online and ready for commands. How can I help?")
    try:
        while True:
            if stt.wake_word_detected_event.is_set():
                tts.speak("Yes?")
                user_prompt = stt.listen_for_command()

                stt.wake_word_detected_event.clear()

                if not user_prompt:
                    continue

                if "goodbye" in user_prompt.lower():
                    tts.speak("Alright, catch you later!")
                    break

                if "play" in user_prompt.lower() and "spotify" in user_prompt.lower():
                    command_data = llm.ask_rilo_for_json(user_prompt)
                    if command_data:
                        spotipy_client.execute_spotify_command(command_data=command_data)
                    else:
                        tts.speak("I had trouble understanding that command")
                else:
                    rilo_response = llm.ask_rilo_for_chat(user_prompt)
                    tts.speak(rilo_response)
            
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nShutting down Rilo.")
    finally:
        if 'stop_listening' in locals() and stop_listening:
            stop_listening(wait_for_stop=False)
        print("Rilo is offline.")

if __name__ == "__main__":
    main()
