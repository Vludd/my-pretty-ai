from pathlib import Path
from sqlalchemy import text, MetaData
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

import app.config as cfg
from app.core.prompt_manager.importer import import_prompt_json
from app.models.prompt import MPrompt
from app.database.base import Base
from app.repositories.prompt import PromptRepository
from app.utils.logger import logger

DATABASE_URL = f"postgresql+asyncpg://{cfg.DB_USER}:{cfg.DB_PASSWORD}@{cfg.DB_HOST}:{cfg.DB_PORT}/{cfg.DB_NAME}"

engine = create_async_engine(DATABASE_URL, future=True, echo=True)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
    autoflush=False
)

SCHEMA_NAME = cfg.DB_SCHEMA
metadata = MetaData(schema=SCHEMA_NAME)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

async def create_default_prompt(session: AsyncSession):
    repo = PromptRepository(session, MPrompt)
    default_prompt_filename = "default_prompt.json"
    
    file_path = Path(__file__).parent.parent.parent / "app" / "data" / "prompts" / default_prompt_filename
    try:
        data: dict = import_prompt_json(file_path)
    except FileNotFoundError as e:
        logger.error(f"{e}")
        return

    data["is_default"] = True
    
    await repo.create_default_prompt(data)

async def init_db():
    import app.models
    
    async with engine.begin() as conn:
        if SCHEMA_NAME != "public":
            await conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA_NAME}"))
        await conn.run_sync(Base.metadata.create_all)
        
    async with AsyncSessionLocal() as session:
        await create_default_prompt(session)
