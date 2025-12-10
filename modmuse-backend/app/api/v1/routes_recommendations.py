# app/api/v1/routes_recommendations.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_async_session
from app.models.domain import PromptCreate, RecommendationResponse
from app.services.recommendation_service import generate_recommendations

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.post("/", response_model=RecommendationResponse)
async def create_recommendations(
    payload: PromptCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Submit a natural-language prompt and receive a ranked list of recommended mods.

    This endpoint performs:
      • OpenAI prompt embedding + keyword extraction
      • Inserts a Prompt history row
      • Vector similarity search against mod embeddings
      • (Fallback) tag/keyword-based search when embeddings missing
      • Compatibility filtering (dependencies, incompatibilities)
      • Sorted + ranked recommendation results
      • Stores results in the Recommendation table

    Returns:
        RecommendationResponse:
            Contains the prompt_id, cleaned keywords, and a list of recommended mods.
    """
    try:
        return await generate_recommendations(payload, session)

    except Exception as e:
        # Prevent leaking internal details to frontend
        raise HTTPException(status_code=500, detail=f"Recommendation error: {str(e)}")