# app/services/game_service.py
from typing import List
from app.models.domain import GameRead


#TODO In Part 3 this will query the database.
def list_supported_games() -> List[GameRead]:
    #TODO Placeholder data for skeleton testing
    return [
        GameRead(
            game_id=1,
            name="Skyrim",
            genre="RPG",
            engine="Creation Engine",
            platform="PC",
        ),
        GameRead(
            game_id=2,
            name="Minecraft",
            genre="Sandbox",
            engine="Custom",
            platform="PC",
        ),
    ]