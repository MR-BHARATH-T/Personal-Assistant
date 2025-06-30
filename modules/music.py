# modules/music.py
import os
import random
from core.speak import speak

def play_music(song_name=None):
    """Play a random or named song from Music folder."""
    music_dir = os.path.expanduser("~\\Music")
    songs = os.listdir(music_dir)

    if song_name:
        songs = [s for s in songs if song_name.lower() in s.lower()]

    if songs:
        song = random.choice(songs)
        os.startfile(os.path.join(music_dir, song))
        speak(f"Playing {song}")
    else:
        speak("No song found.")
