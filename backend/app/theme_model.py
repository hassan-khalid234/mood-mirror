import os
import requests

THEME_MODEL = "facebook/bart-large-mnli"
HF_API_URL = f"https://router.huggingface.co/hf-inference/models/{THEME_MODEL}"
HF_TOKEN = os.getenv("HF_TOKEN")

THEME_LABELS = [
    "justice and vengeance",
    "hope and optimism",
    "responsibility and duty",
    "raw anger and power",
    "fear and darkness",
    "speed and urgency",
    "pride and confidence",
    "balance and neutrality",
]

def classify_theme(text: str) -> dict:
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {"inputs": text, "parameters": {"candidate_labels": THEME_LABELS}}
    response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    result = response.json()
    if isinstance(result, list):
        result = result[0]
    return dict(zip(result["labels"], [round(s, 4) for s in result["scores"]]))