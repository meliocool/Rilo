import speech_recognition as sr
import time

def debug_microphone():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Microphone Debugger Started.")
        print("---------------------------------")
        print("1. Please be quiet for 3 seconds so Ambient Noise can be measured...")
        
        # Measure ambient noise level
        recognizer.adjust_for_ambient_noise(source, duration=3)
        print(f"-> Ambient noise energy threshold set to: {recognizer.energy_threshold:.2f}")
        print("\n2. Now, I will print the energy level every second.")
        print("   - Stay quiet to see the baseline.")
        print("   - Speak normally to see the level when you talk.")
        print("   - This will help you find a good 'energy_threshold' for the main script.")
        print("   - A good value is usually a bit higher than the quiet level, but lower than your speaking level.")
        print("---------------------------------")

        try:
            while True:
                print("\nSay something...")
                try:
                    audio = recognizer.listen(source, timeout=3, phrase_time_limit=3)
                    print("-> I heard something! The current energy threshold is working.")
                except sr.WaitTimeoutError:
                    print("-> Listening timed out. The energy threshold might be too high.")
                
                time.sleep(1)

        except KeyboardInterrupt:
            print("\nDebugger stopped.")

if __name__ == "__main__":
    debug_microphone()