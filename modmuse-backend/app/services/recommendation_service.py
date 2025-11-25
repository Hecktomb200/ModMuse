# app/services/recommendation_service.py
from datetime import datetime
from typing import List

from app.models.domain import (
    PromptCreate,
    PromptRead,
    RecommendationItem,
    RecommendationResponse,
    ModRead,
    TagRead,
)


def generate_recommendations(prompt: PromptCreate) -> RecommendationResponse:
    """
    Placeholder implementation.
    Later this will:
      - Extract keywords using an AI model
      - Query the mod DB using tags, dependencies, incompatibilities
      - Rank and return recommendations
    """
    fake_prompt_id = 1

    # Fake keyword extraction for now
    extracted_keywords: List[str] = ["survival", "hardcore", "Skyrim"]

    prompt_read = PromptRead(
        prompt_id=fake_prompt_id,
        user_prompt=prompt.user_prompt,
        created_at=datetime.utcnow(),
        extracted_keywords=extracted_keywords,
        model_version="stub-0.1",
    )

    # Dummy mod + recommendation
    dummy_mod = ModRead(
        mod_id=101,
        name="Frostfall - Hypothermia Camping Survival",
        description="Adds hypothermia, camping, and survival mechanics to Skyrim.",
        source_url="https://www.nexusmods.com/skyrim/mods/11163",
        version="3.4.1",
        game_id=1,
        tags=[
            TagRead(tag_id=1, name="survival"),
            TagRead(tag_id=2, name="immersion"),
        ],
    )

    rec_item = RecommendationItem(
        rec_id=1,
        prompt_id=fake_prompt_id,
        mod=dummy_mod,
        relevance_score=0.95,
        rank_order=1,
    )

    return RecommendationResponse(
        prompt=prompt_read,
        recommendations=[rec_item],
    )