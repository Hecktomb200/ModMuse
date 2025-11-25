# app/api/v1/routes_recommendations.py
from fastapi import APIRouter

from app.models.domain import PromptCreate, RecommendationResponse
from app.services.recommendation_service import generate_recommendations

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.post("/", response_model=RecommendationResponse)
def create_recommendations(payload: PromptCreate):
    """
    Submit a natural-language prompt and get a recommended set of mods.

    In Part 2 this is a stub that returns hard-coded data.
    In later parts it will:
      - Call an AI model to extract intent/keywords
      - Query the mod database
      - Rank compatible mods
    """
    return generate_recommendations(payload)