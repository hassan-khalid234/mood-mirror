from transformers import pipeline
from functools import lru_cache

MODEL_NAME = "j-hartmann/emotion-english-distilroberta-base"

@lru_cache(maxsize=1)
def get_classifier():
    """
    Loaded once, cached for the lifetime of the process.
    lru_cache with maxsize=1 acts as a singleton here.
    """
    return pipeline(
        "text-classification",
        model=MODEL_NAME,
        top_k=None  # Return scores for ALL 7 emotion labels, not just top 1
    )

def classify_emotion(text: str) -> dict:
    """
    Passes text through the DistilRoBERTa emotion classifier.
    Returns dictionary of label to normalized score (0.0 - 1.0).
    """
    classifier = get_classifier()
    results = classifier(text)[0]  # list of {"label": ..., "score": ...}
    return {r["label"]: round(r["score"], 4) for r in results}