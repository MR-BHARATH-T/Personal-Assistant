import streamlit as st
import random
import time
import os
import datetime
import base64
import cv2
from streamlit_mic_recorder import mic_recorder
from streamlit_chat import message
import pywhatkit as kit
from streamlit_player import st_player

from core.speak import speak
from core.gemini import ask_gemini
from core.did import generate_avatar_video
from modules import wikipedia_module, music, notes, youtube, emotion

# ================== Config ==================
st.set_page_config(page_title="Bro Assistant", layout="centered")
st.title("🤖 Bro Voice Assistant")
AVATAR = "https://media.giphy.com/media/jQmVFypWInKCc/giphy.gif"
WAVE_GIF = "https://media.giphy.com/media/iicDrNGWxHmDrIni6j/giphy.gif"
LIPSYNC_AVATAR = "https://media.giphy.com/media/BHNfhgU63qrks/giphy.gif"

os.makedirs("data", exist_ok=True)

# ================== Session ==================
if "history" not in st.session_state:
    st.session_state.history = []
if "chat" not in st.session_state:
    st.session_state.chat = []
if "muted" not in st.session_state:
    st.session_state.muted = False
if "last_audio" not in st.session_state:
    st.session_state.last_audio = None

# ================== Utility ==================
def play_audio_file(path):
    with open(path, "rb") as audio_file:
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format="audio/mp3")

def show_waveform():
    for _ in range(10):
        st.markdown("🔉 " * random.randint(4, 10))
        time.sleep(0.1)

def show_face_camera(animated=False):
    stframe = st.empty()
    cap = cv2.VideoCapture(0)
    while animated:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.putText(frame, "😄 Talking...", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        stframe.image(frame, channels="BGR", use_column_width=True)
    cap.release()

def send_whatsapp_msg(number, msg):
    now = datetime.datetime.now()
    kit.sendwhatmsg(number, msg, now.hour, now.minute + 2)
    st.success(f"Message scheduled to {number}")

def to_display_str(obj):
    if isinstance(obj, bytes):
        return obj.decode('utf-8', errors='replace')
    return str(obj)

# ================== Voice Input ==================
voice_text = mic_recorder(start_prompt="🎤 Click to speak", stop_prompt="🛑 Stop Recording", just_once=True)
user_input = st.text_input("Type something...")
final_input = voice_text or user_input

if final_input:
    st.markdown(f"🗣️ **You:** {final_input}")
    st.session_state.chat.append({"role": "user", "content": final_input})
    st.session_state.history.append({"role": "user", "text": final_input})

    # Handle Commands
    if "wikipedia" in final_input:
        result = wikipedia_module.search_wikipedia(final_input.replace("wikipedia", ""))
    elif "note" in final_input:
        notes.add_note(final_input)
        result = "Note saved!"
    elif "play music" in final_input:
        music.play_music()
        result = "Playing music..."
    elif "youtube" in final_input:
        yt_link = youtube.search_youtube(final_input.replace("youtube", ""))
        if yt_link:
            st_player(yt_link)
            result = f"Playing video: {yt_link}"
        else:
            result = "Couldn't find a video."
    elif "play video" in final_input:
        st.video("sample_video.mp4")
        result = "Playing a local video..."
    else:
        result = ask_gemini(final_input)

    # Decode result if bytes
    if isinstance(result, bytes):
        result = result.decode('utf-8', errors='replace')

    st.session_state.chat.append({"role": "assistant", "content": result})
    st.session_state.history.append({"role": "assistant", "text": result})
    st.markdown(f"🤖 **Bro:** {result}")

    # Waveform & Lip-sync Avatar
    if not st.session_state.muted:
        st.image(WAVE_GIF, caption="🎧 Talking...", width=300)
        st.image(LIPSYNC_AVATAR, caption="🧍 Lip-syncing...", width=200)
        show_waveform()

    # Speak
    audio_path = speak(result)
    st.session_state.last_audio = audio_path

    if not st.session_state.muted:
        play_audio_file(audio_path)

    # Generate avatar video using D-ID
    avatar_path = generate_avatar_video(result)
    if avatar_path:
        st.video(avatar_path)

# ================== Chat Log ==================
st.subheader("💬 Chat Log")
for msg in st.session_state.chat:
    content = to_display_str(msg["content"])
    message(content, is_user=(msg["role"] == "user"))

# ================== Mute / Replay ==================
col1, col2 = st.columns(2)

with col1:
    if st.button("🔇 Mute"):
        st.session_state.muted = True
        st.info("Muted.")

with col2:
    if st.button("🔁 Replay") and st.session_state.last_audio:
        play_audio_file(st.session_state.last_audio)

# ================== WhatsApp ==================
with st.expander("📱 WhatsApp"):
    number = st.text_input("Phone Number (+91...)")
    message_txt = st.text_area("Your message")
    if st.button("📤 Send WhatsApp Message"):
        if number and message_txt:
            send_whatsapp_msg(number, message_txt)

# ================== Face Animation ==================
if st.checkbox("🧍 Show Face Animations"):
    show_face_camera(animated=True)

# ================== Emotion Detection ==================
if st.button("🧠 Detect My Emotion"):
    detected = emotion.detect_emotion()
    st.success(f"Detected Emotion: {detected}")

    # Save emotion to log
    emotion.save_emotion_to_history(detected)

    # Emotion-based response
    msg, yt = emotion.emotion_response_action(detected)
    st.info(msg)

    if yt:
        st_player(yt)
    else:
        mood_result = music.play_emotion_music(detected)
        st.info(mood_result)

# ================== Save Chat ==================
if st.button("💾 Save Chat History"):
    filename = f"chat_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(f"data/{filename}", "w", encoding="utf-8") as f:
        for msg in st.session_state.history:
            f.write(f"{msg['role'].capitalize()}: {msg['text']}\n")
    st.success(f"Saved to data/{filename}")

# ================== Emotion Analytics ==================
with st.expander("📊 Emotion Stats"):
    df = emotion.get_emotion_stats()
    if not df.empty:
        st.subheader("💡 Emotion Counts")
        st.bar_chart(df["emotion"].value_counts())

        st.subheader("🗓️ Filter by Date Range")
        start_date = st.date_input("Start Date", df["timestamp"].min().date())
        end_date = st.date_input("End Date", df["timestamp"].max().date())

        mask = (df["timestamp"].dt.date >= start_date) & (df["timestamp"].dt.date <= end_date)
        filtered = df[mask]

        if not filtered.empty:
            st.subheader("📉 Mood Trend Over Time")
            hourly = filtered.copy()
            hourly["hour"] = hourly["timestamp"].dt.floor("H")
            mood_counts = hourly.groupby(["hour", "emotion"]).size().unstack(fill_value=0)
            st.line_chart(mood_counts)
        else:
            st.info("No emotions detected in selected range.")
    else:
        st.info("No emotion data found yet.")
