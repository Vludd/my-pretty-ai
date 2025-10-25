from sqlalchemy import text, MetaData
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

import app.config as cfg

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
Base = declarative_base(metadata=metadata)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

async def init_db():
    import app.models
    async with engine.begin() as conn:
        if SCHEMA_NAME != "public":
            await conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA_NAME}"))
        await conn.run_sync(Base.metadata.create_all)