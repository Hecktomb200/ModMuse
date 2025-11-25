# app/main.py
from fastapi import FastAPI
from app.api.v1.routes_health import router as health_router
from app.api.v1.routes_games import router as games_router
from app.api.v1.routes_recommendations import router as recommendations_router

app = FastAPI(
    title="ModMuse API",
    version="0.1.0",
    description="Backend API for the ModMuse AI-powered mod recommendation system.",
)


# Mount versioned API
app.include_router(health_router, prefix="/api/v1")
app.include_router(games_router, prefix="/api/v1")
app.include_router(recommendations_router, prefix="/api/v1")


@app.get("/", tags=["root"])
def read_root():
    return {"message": "Welcome to the ModMuse API. See /docs for details."}