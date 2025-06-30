# core/gemini.py
import google.generativeai as genai
from config import GEMINI_API_KEY
from core.speak import speak

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

def ask_gemini(prompt: str) -> str:
    try:
        response = model.generate_content(prompt)
        answer = response.text.strip()
        return answer
    except Exception as e:
        return f"Gemini failed: {e}"
