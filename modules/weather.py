# modules/weather.py
import requests
from core.speak import speak
from config import WEATHER_API_KEY, DEFAULT_CITY

def get_weather(city=DEFAULT_CITY):
    """Fetch weather from OpenWeatherMap."""
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        res = requests.get(url).json()
        if res.get("cod") != 200:
            speak("City not found.")
            return
        temp = res["main"]["temp"]
        desc = res["weather"][0]["description"]
        speak(f"The weather in {city} is {desc} with {temp}°C.")
    except Exception:
        speak("Couldn't fetch the weather.")
