from openai import AsyncOpenAI
import os

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def embed_text(text: str) -> list[float]:
    """Generate an embedding vector for text."""
    response = await client.embeddings.create(
        model="text-embedding-3-large",
        input=text
    )
    return response.data[0].embedding