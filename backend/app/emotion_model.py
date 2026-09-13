import os
import requests

EMOTION_MODEL = "j-hartmann/emotion-english-distilroberta-base"
HF_API_URL = f"https://router.huggingface.co/hf-inference/models/{EMOTION_MODEL}"
HF_TOKEN = os.getenv("HF_TOKEN")

def classify_emotion(text: str) -> dict:
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {"inputs": text}
    response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    results = response.json()[0]
    return {r["label"]: round(r["score"], 4) for r in results}