import os
import requests

THEME_MODEL = "facebook/bart-large-mnli"
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
    url = f"https://api-inference.huggingface.co/models/{THEME_MODEL}"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {"inputs": text, "parameters": {"candidate_labels": THEME_LABELS}}
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    result = response.json()
    # result has "labels" and "scores", both sorted descending
    return dict(zip(result["labels"], [round(s, 4) for s in result["scores"]]))