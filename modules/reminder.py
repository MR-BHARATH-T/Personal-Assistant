# modules/reminder.py
import json
import os
from datetime import datetime
from core.speak import speak

REMINDER_FILE = "data/reminders.json"

def add_reminder(text: str, time: str):
    """Add a new reminder."""
    reminders = load_reminders()
    reminders.append({"text": text, "time": time})
    with open(REMINDER_FILE, "w") as f:
        json.dump(reminders, f, indent=4)
    speak("Reminder added!")

def load_reminders():
    """Load all reminders."""
    if not os.path.exists(REMINDER_FILE):
        return []
    with open(REMINDER_FILE, "r") as f:
        return json.load(f)

def show_reminders():
    """Speak out all reminders."""
    reminders = load_reminders()
    if not reminders:
        speak("You have no reminders.")
        return
    for rem in reminders:
        speak(f"Reminder: {rem['text']} at {rem['time']}")
