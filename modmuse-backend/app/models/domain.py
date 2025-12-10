# app/models/domain.py
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


# ---------- Game ----------

class GameBase(BaseModel):
    game_id: int
    name: str
    genre: Optional[str] = None
    engine: Optional[str] = None
    platform: Optional[str] = None


class GameRead(GameBase):
    pass


# ---------- Tags ----------

class TagRead(BaseModel):
    tag_id: int
    name: str


# ---------- Mods ----------

class ModBase(BaseModel):
    mod_id: int
    name: str
    description: Optional[str] = None
    source_url: Optional[str] = None
    version: Optional[str] = None
    game_id: int


class ModRead(ModBase):
    tags: List[TagRead] = []
    embedding: list[float] | None = None


# ---------- Prompts & Recommendations ----------

class PromptCreate(BaseModel):
    user_prompt: str


class PromptRead(BaseModel):
    prompt_id: int
    user_prompt: str
    created_at: datetime
    extracted_keywords: List[str]
    model_version: str


class RecommendationItem(BaseModel):
    rec_id: int
    prompt_id: int
    mod: ModRead
    relevance_score: float
    rank_order: int


class RecommendationResponse(BaseModel):
    prompt: PromptRead
    recommendations: List[RecommendationItem]