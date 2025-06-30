# modules/notes.py
import os
from core.speak import speak

NOTES_FILE = "data/notes.txt"

def add_note(text: str):
    """Add a note."""
    with open(NOTES_FILE, "a") as f:
        f.write(f"{text}\n")
    speak("Note saved!")

def read_notes():
    """Read all notes."""
    if not os.path.exists(NOTES_FILE):
        speak("No notes found.")
        return
    with open(NOTES_FILE, "r") as f:
        notes = f.readlines()
    for note in notes:
        speak(note.strip())
