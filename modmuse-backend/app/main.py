# app/main.py

import logging
import traceback
from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.routes_health import router as health_router
from app.api.v1.routes_games import router as games_router
from app.api.v1.routes_recommendations import router as recommendations_router

# -----------------------------------------------------------
# 🔥 Enable global debug logging
# -----------------------------------------------------------
logging.basicConfig(level=logging.DEBUG)

app = FastAPI(
    debug=True,
    title="ModMuse API",
    version="0.1.0",
    description="Backend API for the ModMuse AI-powered mod recommendation system.",
)

# -----------------------------------------------------------
# 🔥 CORS: Allow frontend (static index.html) to call backend
# -----------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for demo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------------------------------------
# 🔥 Global exception handler — forces tracebacks to appear
# -----------------------------------------------------------
@app.exception_handler(Exception)
async def all_exception_handler(request: Request, exc: Exception):
    print("\n\n🔥🔥🔥 UNCAUGHT EXCEPTION 🔥🔥🔥")
    traceback.print_exc()
    print("-----------------------------------------------------\n")
    return PlainTextResponse(str(exc), status_code=500)

# -----------------------------------------------------------
# Routers
# -----------------------------------------------------------
app.include_router(health_router, prefix="/api/v1")
app.include_router(games_router, prefix="/api/v1")
app.include_router(recommendations_router, prefix="/api/v1")

@app.get("/", tags=["root"])
def read_root():
    return {"message": "Welcome to the ModMuse API. See /docs for details."}