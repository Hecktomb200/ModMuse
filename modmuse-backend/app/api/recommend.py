from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.api.schemas import PromptRequest
from app.db.session import get_async_session
from app.services.embedding_service import embed_text

router = APIRouter()

@router.post("/recommend")
async def recommend(
    request: PromptRequest,
    session: AsyncSession = Depends(get_async_session)
):
    # 1. Embed user prompt
    emb = await embed_text(request.prompt)

    # 2. Vector similarity search using pgvector `<=>` operator
    query = text("""
        SELECT 
            mod_id,
            name,
            description,
            source_url,
            version,
            (embedding <=> :emb) AS distance
        FROM mod
        ORDER BY embedding <=> :emb
        LIMIT 5;
    """)

    result = await session.execute(query, {"emb": emb})
    mods = result.mappings().all()

    # 3. Format results
    return {
        "prompt": request.prompt,
        "recommendations": [
            {
                "mod_id": row["mod_id"],
                "name": row["name"],
                "description": row["description"],
                "source_url": row["source_url"],
                "version": row["version"],
                "distance": float(row["distance"]),
            }
            for row in mods
        ]
    }