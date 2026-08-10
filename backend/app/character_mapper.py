CHARACTER_MAP = {
    "joy": {
        "character": "Spider-Man",
        "theme_color": "#E23636",
        "tagline": "With great power comes great responsibility."
    },
    "sadness": {
        "character": "Batman",
        "theme_color": "#1A1A2E",
        "tagline": "It's not who I am underneath, but what I do that defines me."
    },
    "anger": {
        "character": "The Hulk",
        "theme_color": "#4CAF50",
        "tagline": "Don't make me angry. You wouldn't like me when I'm angry."
    },
    "fear": {
        "character": "Daredevil",
        "theme_color": "#8B0000",
        "tagline": "I'm not afraid of the dark. I am the dark."
    },
    "surprise": {
        "character": "The Flash",
        "theme_color": "#FFD700",
        "tagline": "Life doesn't slow down for anyone."
    },
    "disgust": {
        "character": "Wolverine",
        "theme_color": "#4A4A4A",
        "tagline": "I'm the best there is at what I do."
    },
    "neutral": {
        "character": "Superman",
        "theme_color": "#0072CE",
        "tagline": "Balanced. Grounded. Steady."
    },
}

# Below this confidence, we don't commit to a single character —
# we surface the top 2 candidates instead so the UI can show a
# "mixed feelings" state rather than a falsely confident answer.
CONFIDENCE_THRESHOLD = 0.60


def map_emotion_to_character(emotion_scores: dict) -> dict:
    """
    Takes the full emotion score dict, finds the dominant emotion,
    and returns either a single confident character match, or a
    "mixed" result with the top 2 candidates if confidence is low.
    """
    # Sort emotions by score, descending
    ranked = sorted(emotion_scores.items(), key=lambda kv: kv[1], reverse=True)
    top_emotion, top_confidence = ranked[0]
    second_emotion, second_confidence = ranked[1]

    top_character = CHARACTER_MAP[top_emotion]

    if top_confidence >= CONFIDENCE_THRESHOLD:
        return {
            "status": "confident",
            "dominant_emotion": top_emotion,
            "confidence": top_confidence,
            "character": top_character["character"],
            "theme_color": top_character["theme_color"],
            "tagline": top_character["tagline"],
            "all_scores": emotion_scores,
        }

    # Low confidence — return top 2 as a "mixed" result
    second_character = CHARACTER_MAP[second_emotion]
    return {
        "status": "mixed",
        "dominant_emotion": top_emotion,
        "confidence": top_confidence,
        "character": top_character["character"],
        "theme_color": top_character["theme_color"],
        "tagline": top_character["tagline"],
        "candidates": [
            {
                "emotion": top_emotion,
                "confidence": top_confidence,
                "character": top_character["character"],
                "theme_color": top_character["theme_color"],
            },
            {
                "emotion": second_emotion,
                "confidence": second_confidence,
                "character": second_character["character"],
                "theme_color": second_character["theme_color"],
            },
        ],
        "all_scores": emotion_scores,
    }