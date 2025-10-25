from datetime import datetime, timezone

from sqlalchemy import Column, ForeignKey, Integer, DateTime, TEXT

from app.database import Base
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
        comment="Первичный ключ записи"
    )
    
    conversation_id = Column(
        ForeignKey(FK_conversations_id), 
        nullable=False,
        comment=f"Внешний ключ к {FK_conversations_id}"
    )
    
    prompt = Column(
        TEXT,
        nullable=False,
        comment="Текст промпта"
    )
    
    response = Column(
        TEXT, 
        nullable=True,
        comment="Ответ на промпт"
    )
    
    input_tokens = Column(
        Integer,
        nullable=True,
        comment="Входящие токены"
    )
    
    output_tokens = Column(
        Integer,
        nullable=True,
        comment="Исходящие токены"
    )
    
    total_tokens = Column(
        Integer,
        nullable=True,
        comment="Потраченные токены на весь запрос"
    )
    
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        comment="Дата создания записи"
    )
