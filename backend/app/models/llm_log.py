from datetime import datetime, timezone

from sqlalchemy import TEXT, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

import app.config as cfg
from app.database.base import Base

FK_conversations_id = "conversations.id"

class MLLMLog(Base):
    __tablename__ = "llm_logs"
    __table_args__ = ({"schema": cfg.DB_SCHEMA} if cfg.DB_SCHEMA != "public" else {})
    
    id: Mapped[int] = mapped_column(
        Integer, 
        primary_key=True, 
        index=True,
        comment="PK"
    )
    
    conversation_id: Mapped[int] = mapped_column(
        ForeignKey(FK_conversations_id), 
        nullable=False,
        comment=f"FK {FK_conversations_id}"
    )
    
    prompt: Mapped[str] = mapped_column(
        TEXT,
        nullable=False,
        comment="Prompt text"
    )
    
    response: Mapped[str] = mapped_column(
        TEXT, 
        nullable=True,
        comment="Response"
    )
    
    input_tokens: Mapped[int] = mapped_column(
        Integer,
        nullable=True,
        comment="Input tokens"
    )
    
    output_tokens: Mapped[int] = mapped_column(
        Integer,
        nullable=True,
        comment="Output tokens"
    )
    
    total_tokens: Mapped[int] = mapped_column(
        Integer,
        nullable=True,
        comment="Spent tokens for the entire request"
    )
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        comment="Created At"
    )
