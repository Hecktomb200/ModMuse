# app/api/v1/routes_games.py
from typing import List

from fastapi import APIRouter

from app.models.domain import GameRead
from app.services.game_service import list_supported_games

router = APIRouter(prefix="/games", tags=["games"])


@router.get("/", response_model=List[GameRead])
def get_games():
    """
    List all supported games that ModMuse can recommend mods for.
    """
    return list_supported_games()