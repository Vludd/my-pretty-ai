from datetime import datetime, timezone
from uuid import UUID as PyUUID
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

import app.config as cfg
from app.database.base import Base

FK_users_id = "users.id"

class MPrompt(Base):
    __tablename__ = "prompts"
    __table_args__ = ({"schema": cfg.DB_SCHEMA} if cfg.DB_SCHEMA != "public" else {})
    
    id: Mapped[int] = mapped_column(
        Integer, 
        primary_key=True, 
        index=True,
        comment="PK"
    )
    
    public_id: Mapped[PyUUID] = mapped_column(
        PGUUID(as_uuid=True),
        unique=True,
        index=True,
        nullable=False,
        default=uuid4,
        comment="Public UUID of prompt"
    )
    
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(FK_users_id), 
        nullable=True,
        comment=f"FK {FK_users_id}"
    )
    
    name: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="Name of prompt"
    )
    
    layers: Mapped[dict] = mapped_column(
        JSONB, 
        nullable=True,
        comment="Layers of prompt"
    )
    
    is_default: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        comment="Prompt is default?"
    )
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        comment="Created At"
    )
    
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        comment="Updated At"
    )
