# modules/screenshot.py
import pyautogui
import os
from core.speak import speak

def take_screenshot():
    """Takes a screenshot and saves it in Pictures folder."""
    img = pyautogui.screenshot()
    path = os.path.expanduser("~\\Pictures\\screenshot.png")
    img.save(path)
    speak(f"Screenshot saved at {path}")
    print(f"✅ Screenshot saved: {path}")
