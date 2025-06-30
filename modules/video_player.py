# modules/video_player.py
import os
import random
from core.speak import speak

def play_video(video_name=None):
    """Play video from Videos folder."""
    path = os.path.expanduser("~\\Videos")
    videos = os.listdir(path)

    if video_name:
        videos = [v for v in videos if video_name.lower() in v.lower()]

    if videos:
        video = random.choice(videos)
        os.startfile(os.path.join(path, video))
        speak(f"Playing {video}")
    else:
        speak("No video found.")
