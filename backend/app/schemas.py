from pydantic import BaseModel, Field
from typing import Optional, List, Literal


class TextInput(BaseModel):
    text: str = Field(..., min_length=1, max_length=1000)


class CandidateCharacter(BaseModel):
    emotion: str
    confidence: float
    character: str
    theme_color: str


class CharacterResponse(BaseModel):
    status: Literal["confident", "mixed"]
    dominant_emotion: str
    confidence: float
    character: str
    theme_color: str
    tagline: str
    all_scores: dict
    candidates: Optional[List[CandidateCharacter]] = None