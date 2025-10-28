from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

import app.config as cfg

from app.routes import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- startup ---
    # >
    yield
    # >
    # --- shutdown ---

app = FastAPI(
    title=cfg.APP_NAME,
    lifespan=lifespan,
    version="0.1.1"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
