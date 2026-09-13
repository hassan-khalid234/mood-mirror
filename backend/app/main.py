from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.emotion_model import classify_emotion
from app.theme_model import classify_theme
from app.character_mapper import map_to_character
from app.schemas import TextInput, CharacterResponse

load_dotenv()

app = FastAPI(
    title="Mood Mirror API",
    description="Detects emotion in text and maps it to a comic character archetype",
    version="1.0.0"
)

# Enable CORS for local and future frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"status": "ok", "service": "mood-mirror-api"}

@app.post("/analyze", response_model=CharacterResponse)
def analyze_text(payload: TextInput):
    try:
        emotion_scores = classify_emotion(payload.text)
        theme_scores = classify_theme(payload.text)
        result = map_to_character(emotion_scores, theme_scores)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))