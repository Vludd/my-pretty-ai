from datetime import datetime, timezone

from sqlalchemy import Column, ForeignKey, Integer, DateTime, TEXT

from app.database.base import Base
import app.config as cfg

TABLENAME = "llm_logs"
FK_conversations_id = "conversations.id"

class MLLMLog(Base):
    __tablename__ = TABLENAME
    __table_args__ = ({"schema": cfg.DB_SCHEMA} if cfg.DB_SCHEMA != "public" else {})
    
    id = Column(
        Integer, 
        primary_key=True, 
        index=True,
        comment="PK"
    )
    
    conversation_id = Column(
        ForeignKey(FK_conversations_id), 
        nullable=False,
        comment=f"FK {FK_conversations_id}"
    )
    
    prompt = Column(
        TEXT,
        nullable=False,
        comment="Prompt text"
    )
    
    response = Column(
        TEXT, 
        nullable=True,
        comment="Response"
    )
    
    input_tokens = Column(
        Integer,
        nullable=True,
        comment="Input tokens"
    )
    
    output_tokens = Column(
        Integer,
        nullable=True,
        comment="Output tokens"
    )
    
    total_tokens = Column(
        Integer,
        nullable=True,
        comment="Spent tokens for the entire request"
    )
    
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        comment="Created At"
    )
