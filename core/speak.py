# core/speak.py
import pyttsx3
import os
import tempfile
from gtts import gTTS
import os
import uuid


engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)
engine.setProperty("rate", 150)

AUDIO_DIR = "data/audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

def speak(text: str) -> str:
    """Use gTTS to convert text to speech and return audio path."""
    filename = f"{uuid.uuid4()}.mp3"
    path = os.path.join(AUDIO_DIR, filename)
    tts = gTTS(text)
    tts.save(path)
    print(f"🔊 Speaking: {text}")
    return path

def speak(text: str, play_audio=True) -> None:
    print(f"🤖 {text}")
    if play_audio:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
            engine.save_to_file(text, f.name)
            engine.runAndWait()
            return f.name  # Return path for GUI to use
    else:
        engine.say(text)
        engine.runAndWait()
