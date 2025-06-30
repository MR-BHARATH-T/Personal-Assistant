# modules/youtube.py
import webbrowser
from core.speak import speak

def play_youtube(query=""):
    """Plays YouTube or searches if query given."""
    if query:
        url = f"https://www.youtube.com/results?search_query={query}"
        speak(f"Searching YouTube for {query}")
    else:
        url = "https://www.youtube.com"
        speak("Opening YouTube")
    webbrowser.open(url)

from youtubesearchpython import VideosSearch

def search_youtube(query, max_results=1):
    videos = VideosSearch(query, limit=max_results).result()["result"]
    if videos:
        return videos[0]["link"]
    return None
