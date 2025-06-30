# modules/file_search.py
import os
from core.speak import speak

def search_file(filename: str, search_dir: str = "C:\\"):
    """Search for a file in a given directory."""
    speak(f"Searching for {filename}. This might take a while.")
    for root, dirs, files in os.walk(search_dir):
        if filename in files:
            path = os.path.join(root, filename)
            speak(f"Found file at {path}")
            print(path)
            return path
    speak("File not found.")
    return None
