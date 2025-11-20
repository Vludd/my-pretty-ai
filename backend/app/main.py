from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.routes import api_router
from app.database import init_db
from app.core.exception_handlers import setup_exception_handlers

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- startup ---
    await init_db()
    yield
    # --- shutdown ---
    pass

app = FastAPI(
    lifespan=lifespan,
    version="0.3.0"
)

setup_exception_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")
