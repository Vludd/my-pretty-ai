from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.exception_handlers import setup_exception_handlers
from app.core.middleware import request_logging_middleware
from app.database import init_db
from app.routes import api_router
from app.utils.logger import setup_logging

setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- startup ---
    await init_db()
    yield
    # --- shutdown ---
    pass

app = FastAPI(
    lifespan=lifespan,
    version="0.4.0"
)

setup_exception_handlers(app)

app.middleware("http")(request_logging_middleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")
