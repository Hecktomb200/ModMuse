# app/core/config.py
from pydantic import BaseModel
import os


class Settings(BaseModel):
    api_version: str = "v1"
    project_name: str = "ModMuse"
    #TODO DB + OpenAI settings will be added in Part 3/4.
    database_url: str | None = os.getenv("DATABASE_URL")
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")


settings = Settings()