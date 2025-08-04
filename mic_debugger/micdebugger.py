import speech_recognition as sr
import time

def debug_microphone():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Microphone Debugger Started.")
        print("---------------------------------")
        print("Measuring Ambient Noise...")
        
        # Measure ambient noise level
        recognizer.adjust_for_ambient_noise(source, duration=3)
        print(f"-> Ambient noise energy threshold set to: {recognizer.energy_threshold:.2f}")
        print("\n2. Energy Level will be printed every second.")
        print("   - A good value is usually a bit higher than the quiet level, but lower than speaking level.")
        print("---------------------------------")

        try:
            while True:
                print("\nSay something...")
                try:
                    audio = recognizer.listen(source, timeout=3, phrase_time_limit=3)
                    print("-> Heard you twin! The current energy threshold is working.")
                except sr.WaitTimeoutError:
                    print("-> Listening timed out. The energy threshold might be too high.")
                
                time.sleep(1)

        except KeyboardInterrupt:
            print("\nDebugger stopped.")

if __name__ == "__main__":
    debug_microphone()