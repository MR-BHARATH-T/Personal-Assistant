# modules/whatsapp.py
import pywhatkit
from core.speak import speak

def send_whatsapp_message(number: str, message: str, hour: int, minute: int):
    try:
        pywhatkit.sendwhatmsg(number, message, hour, minute)
        speak("WhatsApp message scheduled successfully.")
    except Exception as e:
        speak("Unable to send WhatsApp message.")
        print(e)
