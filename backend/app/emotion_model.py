import os
import requests

EMOTION_MODEL = "j-hartmann/emotion-english-distilroberta-base"
HF_TOKEN = os.getenv("HF_TOKEN")

def classify_emotion(text: str) -> dict:
    url = f"https://api-inference.huggingface.co/models/{EMOTION_MODEL}"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    response = requests.post(url, headers=headers, json={"inputs": text}, timeout=30)
    response.raise_for_status()
    results = response.json()[0]
    return {r["label"]: round(r["score"], 4) for r in results}