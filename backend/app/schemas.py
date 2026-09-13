from pydantic import BaseModel, Field
from typing import Optional, List, Literal


class TextInput(BaseModel):
    text: str = Field(..., min_length=1, max_length=1000)


class CandidateCharacter(BaseModel):
    character: str
    confidence: float
    theme_color: str


class CharacterResponse(BaseModel):
    status: Literal["confident", "mixed"]
    character: str
    confidence: float
    theme_color: str
    tagline: str
    matched_emotion: str
    matched_theme: str
    all_emotion_scores: dict
    all_theme_scores: dict
    candidates: Optional[List[CandidateCharacter]] = None