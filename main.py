from translator import translate_to_hindi
from speech_to_text import recognize_speech
import pyttsx3

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty("rate", 170)
    engine.say(text)
    engine.runAndWait()

def main():
    while True:
        print("\n----------------------------------")
        print("🎤 Speak in English (say 'stop' to exit)")
        print("----------------------------------")

        english_text = recognize_speech()

        if not english_text:
            print("❌ Could not understand. Try again.")
            continue

        print(f"🗣 You said: {english_text}")

        if "stop" in english_text.lower():
            print("👋 Exiting translator.")
            break

        hindi = translate_to_hindi(english_text)
        print(f"🌐 Hindi: {hindi}")

        print("🔊 Speaking translation...")
        speak(hindi)

if __name__ == "__main__":
    main()
