# modules/wikipedia_module.py
import wikipedia
from core.speak import speak

def search_wikipedia(query: str):
    """Searches Wikipedia for the given query."""
    try:
        speak("Searching Wikipedia...")
        result = wikipedia.summary(query, sentences=2)
        speak(result)
        print(result)
    except wikipedia.exceptions.DisambiguationError:
        speak("Multiple results found. Please be more specific.")
    except Exception:
        speak("I couldn't find anything on Wikipedia.")
