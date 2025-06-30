# core/search.py
import requests
from bs4 import BeautifulSoup
from core.speak import speak
import webbrowser

def search_duckduckgo(query: str) -> str:
    try:
        url = f"https://duckduckgo.com/html/?q={query}"
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(res.text, "html.parser")
        results = soup.find_all("a", class_="result__a", limit=1)
        if results:
            answer = results[0].text.strip()
            link = results[0]["href"]
            speak(f"Top result: {answer}")
            return f"{answer}\n{link}"
        else:
            speak("No result found.")
            return "No result found."
    except Exception as e:
        return f"Error during search: {e}"
