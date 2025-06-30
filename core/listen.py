# core/listen.py
import speech_recognition as sr
from core.speak import speak

def take_command(timeout=5) -> str | None:
    """Listen for a voice command and return it as lowercase text."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        r.pause_threshold = 1
        try:
            audio = r.listen(source, timeout=timeout)
        except sr.WaitTimeoutError:
            speak("⏳ Timeout occurred. Please try again.")
            return None

    try:
        print("🧠 Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(f"🗣️ You said: {query}")
        return query.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't get that.")
    except sr.RequestError:
        speak("Speech recognition service is unavailable.")
    except Exception as e:
        speak(f"Error occurred: {e}")
    return None
