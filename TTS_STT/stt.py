import speech_recognition as sr
import config
import threading

wake_word_detected_event = threading.Event()

def _background_listening_callback(recognizer, audio):
    try:
        text = recognizer.recognize_google(audio)
        # One True solution to weird speech recognition
        if config.WAKE_WORD.lower() in text.lower() or "hey rylo" in text.lower() or "hey Lilo" in text.lower() or "play rylo" in text.lower():
            wake_word_detected_event.set()
    except sr.UnknownValueError:
        pass
    except sr.RequestError as e:
        print(f"Could not request results from Google service; {e}")

def start_background_listening():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
    stop_listening = recognizer.listen_in_background(microphone, _background_listening_callback)
    return stop_listening

def listen_for_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("\nListening for command...")
        recognizer.energy_threshold = config.MIC_ENERGY_THRESHOLD
        recognizer.pause_threshold = config.MIC_PAUSE_THRESHOLD
        try:
            audio = recognizer.listen(source, timeout=8, phrase_time_limit=15)
        except sr.WaitTimeoutError:
            print("Listening timed out. Please try again.")
            return None
    try:
        print("Recognizing...")
        command = recognizer.recognize_google(audio)
        print(f"You said: {command}")
        return command
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand what you said. Please try again.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google service; {e}")
        return None