import os
import json
from typing import List, Optional, Any

from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()

# Use the async OpenAI client everywhere in the backend
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def _safe_extract_text(resp: Any) -> Optional[str]:
    """
    Extracts text from OpenAI Responses safely, without triggering Pylance warnings.

    This function uses isinstance + hasattr so Pylance cannot complain.
    """

    # New Responses API: output -> content -> text
    if hasattr(resp, "output") and resp.output:
        out0 = resp.output[0]
        if hasattr(out0, "content") and out0.content:
            item0 = out0.content[0]
            if hasattr(item0, "text"):
                return item0.text

    # Fallback: older shape
    if hasattr(resp, "output_text"):
        return resp.output_text

    return None

# ---------------------------------------------------------
# 1. Keyword extraction
# ---------------------------------------------------------
async def extract_keywords(prompt: str) -> List[str]:
    """
    Calls OpenAI asynchronously and safely extracts keyword JSON.
    Works with all response formats and silences Pylance.
    """

    try:
        resp = await client.responses.create(
            model="gpt-4o-mini",
            input=f"""
                Extract important keyword tags from the following mod recommendation prompt.
                Return ONLY a JSON array of simple strings, no prose, no markdown.

                Prompt: "{prompt}"
            """
        )

        raw = _safe_extract_text(resp)

        if raw is None:
            raise ValueError("Could not extract text from OpenAI response")

    except Exception as e:
        print("🔥 OPENAI ERROR:", type(e), e)
        raise

    # Cleanup for markdown fences
    raw = raw.replace("```json", "").replace("```", "").strip()

    # JSON first
    try:
        data = json.loads(raw)
        if isinstance(data, list):
            return [str(x).strip() for x in data]
    except Exception:
        pass

    # Fallback
    return [x.strip() for x in raw.split(",") if x.strip()]

# ---------------------------------------------------------
# 2. Embedding function for semantic search
# ---------------------------------------------------------
async def embed_text(text: str) -> List[float]:
    """
    Generate a 1536-dimensional embedding vector for semantic search.
    Compatible with pgvector column: Vector(1536)
    """

    response = await client.embeddings.create(
        model="text-embedding-3-small",
        input=text,
    )

    return response.data[0].embedding
