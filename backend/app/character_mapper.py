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

def map_emotion_to_character(emotion_scores: dict) -> dict:
    """
    Identifies dominant emotion score and returns character archetype details.
    """
    dominant_emotion = max(emotion_scores, key=emotion_scores.get)
    confidence = emotion_scores[dominant_emotion]
    character_data = CHARACTER_MAP[dominant_emotion]

    return {
        "dominant_emotion": dominant_emotion,
        "confidence": confidence,
        "character": character_data["character"],
        "theme_color": character_data["theme_color"],
        "tagline": character_data["tagline"],
        "all_scores": emotion_scores
    }