# app/services/recommendation_service.py

from datetime import datetime
from typing import List, Optional

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.domain import (
    PromptCreate,
    PromptRead,
    RecommendationItem,
    RecommendationResponse,
    ModRead,
    TagRead,
)
from app.db.models_utils.domain import Prompt, Recommendation, Mod, Tag, ModTag
from app.services.ai_services import extract_keywords, embed_text

SKYRIM_GAME_ID = 1  # TODO: update to real game_id for Skyrim


async def generate_recommendations(
    prompt_data: PromptCreate,
    session: AsyncSession
) -> RecommendationResponse:

    try:
        # ---------------------------------------------------------
        # 1. Extract Keywords
        # ---------------------------------------------------------
        extracted_keywords: List[str] = await extract_keywords(prompt_data.user_prompt)
        print("🔥 DEBUG — Extracted keywords:", extracted_keywords)

        # ---------------------------------------------------------
        # 2. Generate Embedding
        # ---------------------------------------------------------
        prompt_embedding: Optional[List[float]] = await embed_text(prompt_data.user_prompt)
        print("🔥 DEBUG — Prompt embedding length:", len(prompt_embedding) if prompt_embedding else None)

        # ---------------------------------------------------------
        # 3. Save Prompt → DB
        # ---------------------------------------------------------
        new_prompt = Prompt(
            user_prompt=prompt_data.user_prompt,
            created_at=datetime.utcnow(),
            extracted_keywords=",".join(extracted_keywords),
            model_version="gpt-4o-mini",
            embedding=prompt_embedding,
        )
        session.add(new_prompt)
        await session.flush()

        # ---------------------------------------------------------
        # 4A. Semantic Search (pgvector) — FILTERED BY GAME
        # ---------------------------------------------------------
        semantic_mods: List[Mod] = []
        semantic_ids: List[int] = []

        if prompt_embedding:
            embed_str = "[" + ",".join(f"{x}" for x in prompt_embedding) + "]"
            vector_query = text("""
                SELECT mod_id
                FROM mod
                WHERE embedding IS NOT NULL
                  AND game_id = :game_id
                ORDER BY embedding <=> :embed
                LIMIT 8;
            """)

            rows = await session.execute(
                vector_query,
                {
                    "embed": embed_str,
                    "game_id": SKYRIM_GAME_ID
                }
            )

            semantic_ids = [row.mod_id for row in rows]

            if semantic_ids:
                result = await session.execute(
                    select(Mod)
                    .options(selectinload(Mod.tags).selectinload(ModTag.tag))
                    .where(Mod.mod_id.in_(semantic_ids))
                )
                semantic_mods = list(result.scalars().all())

        # ---------------------------------------------------------
        # 4B. Keyword Tag Search — ALSO FILTERED BY GAME
        # ---------------------------------------------------------
        keyword_mods: List[Mod] = []
        if extracted_keywords:
            stmt = (
                select(Mod)
                .options(selectinload(Mod.tags).selectinload(ModTag.tag))
                .join(ModTag)
                .join(Tag)
                .where(
                    Mod.game_id == SKYRIM_GAME_ID,
                    Tag.name.in_(extracted_keywords),
                )
            )
            result = await session.execute(stmt)
            keyword_mods = list(result.scalars().unique().all())

        # ---------------------------------------------------------
        # 5. Merge + Deduplicate (semantic first)
        # ---------------------------------------------------------
        final_mods: List[Mod] = []
        seen = set()

        for mod in semantic_mods + keyword_mods:
            if mod.mod_id not in seen:
                seen.add(mod.mod_id)
                final_mods.append(mod)

        # ---------------------------------------------------------
        # 6. Build Recommendation Rows + DTO Objects
        # ---------------------------------------------------------
        recommendation_items: List[RecommendationItem] = []
        rank_counter = 1

        for mod in final_mods:
            tag_names = {t.tag.name for t in mod.tags}
            tag_score = len(set(extracted_keywords).intersection(tag_names))

            # Save Recommendation → DB
            rec = Recommendation(
                prompt_id=new_prompt.prompt_id,
                mod_id=mod.mod_id,
                relevance_score=tag_score,
                rank_order=rank_counter,
            )
            session.add(rec)
            await session.flush()

            mod_read = ModRead(
                mod_id=mod.mod_id,
                name=mod.name,
                description=mod.description,
                source_url=mod.source_url,
                version=mod.version,
                game_id=mod.game_id,
                tags=[TagRead(tag_id=mt.tag_id, name=mt.tag.name) for mt in mod.tags]
            )

            recommendation_items.append(
                RecommendationItem(
                    rec_id=rec.rec_id,
                    prompt_id=new_prompt.prompt_id,
                    mod=mod_read,
                    relevance_score=tag_score,
                    rank_order=rank_counter,
                )
            )

            rank_counter += 1

        # ---------------------------------------------------------
        # 7. Build Response DTO
        # ---------------------------------------------------------
        prompt_read = PromptRead(
            prompt_id=new_prompt.prompt_id,
            user_prompt=new_prompt.user_prompt,
            created_at=new_prompt.created_at,
            extracted_keywords=extracted_keywords,
            model_version=new_prompt.model_version,
        )

        print(f"🔥 DEBUG — Returning {len(recommendation_items)} recommendations.")
        return RecommendationResponse(
            prompt=prompt_read,
            recommendations=recommendation_items,
        )

    except Exception as e:
        print("\n🔥🔥🔥 ERROR INSIDE generate_recommendations() 🔥🔥🔥")
        import traceback
        traceback.print_exc()
        print("---------------------------------------------------------\n")
        raise
