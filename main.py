# main.py
from core.speak import speak
from core.listen import take_command
from core.search import open_website
from core.gemini import ask_gemini

from modules import (
    screenshot, wikipedia_module, music, youtube, video_player,
    reminder, notes, weather, emailer, whatsapp, file_search
)

import datetime
import os

def wish_user():
    hour = datetime.datetime.now().hour
    if 4 <= hour < 12:
        greet = "Good morning"
    elif 12 <= hour < 16:
        greet = "Good afternoon"
    elif 16 <= hour < 21:
        greet = "Good evening"
    else:
        greet = "Good night"
    speak(f"{greet}, bro! I'm ready to help you.")

def run_assistant():
    wish_user()

    while True:
        query = take_command()
        if not query:
            continue

        if "time" in query:
            speak(datetime.datetime.now().strftime("%I:%M %p"))

        elif "date" in query:
            now = datetime.datetime.now()
            speak(f"Today is {now.day} {now.strftime('%B')} {now.year}")

        elif "wikipedia" in query:
            wikipedia_module.search_wikipedia(query.replace("wikipedia", "").strip())

        elif "play music" in query:
            music.play_music(query.replace("play music", "").strip())

        elif "screenshot" in query:
            screenshot.take_screenshot()

        elif "youtube" in query:
            youtube.play_youtube(query.replace("youtube", "").strip())

        elif "video" in query:
            video_player.play_video(query.replace("video", "").strip())

        elif "open" in query:
            site = query.replace("open", "").strip()
            open_website(site)

        elif "remind me" in query:
            speak("What should I remind you?")
            text = take_command()
            speak("When should I remind you?")
            time = take_command()
            if text and time:
                reminder.add_reminder(text, time)

        elif "show reminders" in query:
            reminder.show_reminders()

        elif "write note" in query:
            speak("What should I note?")
            note = take_command()
            if note:
                notes.add_note(note)

        elif "show notes" in query:
            notes.read_notes()

        elif "weather" in query:
            speak("Which city?")
            city = take_command()
            weather.get_weather(city)

        elif "email" in query:
            speak("To whom?")
            to = take_command()
            speak("Subject?")
            subject = take_command()
            speak("Message?")
            message = take_command()
            emailer.send_email(to, subject, message)

        elif "whatsapp" in query:
            speak("Enter number with country code:")
            number = input("Number: ")
            speak("What should I send?")
            msg = take_command()
            speak("Hour?")
            hour = int(input("Hour (24h): "))
            speak("Minute?")
            minute = int(input("Minute: "))
            whatsapp.send_whatsapp_message(number, msg, hour, minute)

        elif "find file" in query:
            speak("What's the file name?")
            filename = take_command()
            if filename:
                file_search.search_file(filename)

        elif "gemini" in query:
            response = ask_gemini(query.replace("gemini", "").strip())
            speak(response)

        elif "exit" in query or "offline" in query or "quit" in query:
            speak("Alright bro, going offline. Catch you later!")
            break

        else:
            speak("I didn't get that. Wanna ask Gemini?")
            response = ask_gemini(query)
            speak(response)

if __name__ == "__main__":
    run_assistant()
