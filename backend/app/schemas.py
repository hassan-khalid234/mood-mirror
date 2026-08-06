from pydantic import BaseModel, Field

class TextInput(BaseModel):
    text: str = Field(..., min_length=1, max_length=1000)

class CharacterResponse(BaseModel):
    dominant_emotion: str
    confidence: float
    character: str
    theme_color: str
    tagline: str
    all_scores: dict