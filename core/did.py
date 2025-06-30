import requests
import json

DID_API_KEY = "your_did_api_key_here"  # Replace this

def generate_avatar_video(text, output_path="avatar_video.mp4"):
    url = "https://api.d-id.com/talks"

    payload = {
        "script": {
            "type": "text",
            "input": text,
            "provider": {"type": "microsoft", "voice_id": "en-US-JennyNeural"},
            "ssml": False
        },
        "source_url": "https://create-images-results.d-id.com/default-character.png"
    }

    headers = {
        "Authorization": f"Bearer {DID_API_KEY}",
        "Content-Type": "application/json"
    }

    res = requests.post(url, headers=headers, json=payload)
    video_url = res.json().get("result_url")

    if not video_url:
        print("D-ID failed:", res.text)
        return None

    video = requests.get(video_url)
    with open(output_path, "wb") as f:
        f.write(video.content)

    return output_path
