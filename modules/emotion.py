import datetime
import os
import json

def save_emotion_to_history(emotion):
    os.makedirs("data", exist_ok=True)
    path = "data/emotion_log.json"
    now = datetime.datetime.now().isoformat()

    data = {}
    if os.path.exists(path):
        with open(path, "r") as f:
            data = json.load(f)

    data[now] = emotion

    with open(path, "w") as f:
        json.dump(data, f, indent=2)

import pandas as pd

def get_emotion_stats():
    path = "data/emotion_log.json"
    if not os.path.exists(path):
        return pd.DataFrame()

    with open(path, "r") as f:
        data = json.load(f)

    df = pd.DataFrame(list(data.items()), columns=["timestamp", "emotion"])
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df


def emotion_response_action(emotion):
    actions = {
        "happy": ("Playing your happy vibe track!", "https://www.youtube.com/watch?v=ZbZSe6N_BXs"),  # Pharrell - Happy
        "sad": ("Let me lift your mood ☀️", "https://www.youtube.com/watch?v=ltrMfT4Qz5Y"),  # Cheer up song
        "angry": ("Here's something to calm you down 🧘", "https://www.youtube.com/watch?v=2OEL4P1Rz04"),
        "neutral": ("Feeling chill? Let me know if you need anything!", None),
        "surprise": ("Whoa! Here's a fun random video 🎉", "https://www.youtube.com/watch?v=DLzxrzFCyOs"),
        "fear": ("Stay calm bro, take a breath 🌿", "https://www.youtube.com/watch?v=inpok4MKVLM")
    }
    return actions.get(emotion, ("Hmm... not sure how to react 😅", None))
