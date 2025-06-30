# modules/emailer.py
import smtplib
from core.speak import speak
from config import EMAIL_ADDRESS, EMAIL_PASSWORD

def send_email(to, subject, message):
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            body = f"Subject: {subject}\n\n{message}"
            server.sendmail(EMAIL_ADDRESS, to, body)
        speak("Email has been sent.")
    except Exception as e:
        speak("Failed to send email.")
        print(e)
