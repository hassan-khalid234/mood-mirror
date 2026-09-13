CHARACTER_MAP = {
    "Spider-Man": {
        "emotion": "joy",
        "theme": "responsibility and duty",
        "theme_color": "#E23636",
        "tagline": "With great power comes great responsibility.",
    },
    "Batman": {
        "emotion": "anger",
        "theme": "justice and vengeance",
        "theme_color": "#1A1A2E",
        "tagline": "It's not who I am underneath, but what I do that defines me.",
    },
    "The Hulk": {
        "emotion": "anger",
        "theme": "raw anger and power",
        "theme_color": "#4CAF50",
        "tagline": "Don't make me angry. You wouldn't like me when I'm angry.",
    },
    "Daredevil": {
        "emotion": "fear",
        "theme": "fear and darkness",
        "theme_color": "#8B0000",
        "tagline": "I'm not afraid of the dark. I am the dark.",
    },
    "The Flash": {
        "emotion": "surprise",
        "theme": "speed and urgency",
        "theme_color": "#FFD700",
        "tagline": "Life doesn't slow down for anyone.",
    },
    "Wolverine": {
        "emotion": "disgust",
        "theme": "pride and confidence",
        "theme_color": "#4A4A4A",
        "tagline": "I'm the best there is at what I do.",
    },
    "Superman": {
        "emotion": "joy",
        "theme": "hope and optimism",
        "theme_color": "#0072CE",
        "tagline": "Balanced. Grounded. Steady.",
    },
}

# Weighting: theme matters more than raw emotion for character identity,
# since two characters can share an emotion (Spider-Man & Superman both "joy")
# but differ entirely in theme.
EMOTION_WEIGHT = 0.35
THEME_WEIGHT = 0.65
CONFIDENCE_THRESHOLD = 0.55


def map_to_character(emotion_scores: dict, theme_scores: dict) -> dict:
    ranked = []
    for name, profile in CHARACTER_MAP.items():
        e_score = emotion_scores.get(profile["emotion"], 0)
        t_score = theme_scores.get(profile["theme"], 0)
        combined = (e_score * EMOTION_WEIGHT) + (t_score * THEME_WEIGHT)
        ranked.append((name, combined, e_score, t_score))

    ranked.sort(key=lambda x: x[1], reverse=True)
    top_name, top_score, top_e, top_t = ranked[0]
    top_profile = CHARACTER_MAP[top_name]

    result = {
        "character": top_name,
        "confidence": round(top_score, 4),
        "theme_color": top_profile["theme_color"],
        "tagline": top_profile["tagline"],
        "matched_emotion": top_profile["emotion"],
        "matched_theme": top_profile["theme"],
        "all_emotion_scores": emotion_scores,
        "all_theme_scores": theme_scores,
    }

    if top_score >= CONFIDENCE_THRESHOLD:
        result["status"] = "confident"
    else:
        second_name, second_score, _, _ = ranked[1]
        second_profile = CHARACTER_MAP[second_name]
        result["status"] = "mixed"
        result["candidates"] = [
            {"character": top_name, "confidence": round(top_score, 4), "theme_color": top_profile["theme_color"]},
            {"character": second_name, "confidence": round(second_score, 4), "theme_color": second_profile["theme_color"]},
        ]

    return result