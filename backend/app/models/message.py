import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, TEXT, Enum
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base
import app.config as cfg
from app.types.messages import SenderType

TABLENAME = "messages"
FK_conversations_id = "conversations.id"

class MMessage(Base):
    __tablename__ = TABLENAME
    __table_args__ = ({"schema": cfg.DB_SCHEMA} if cfg.DB_SCHEMA != "public" else {})
    
    id = Column(
        Integer, 
        primary_key=True, 
        index=True,
        comment="Первичный ключ записи"
    )
    
    public_id = Column(
        UUID(as_uuid=True),
        unique=True,
        index=True,
        nullable=False,
        default=uuid.uuid4,
        comment="Публичный UUID сообщения"
    )
    
    conversation_id = Column(
        ForeignKey(FK_conversations_id), 
        nullable=False,
        comment=f"Внешний ключ к {FK_conversations_id}"
    )
    
    sender_type = Column(
        Enum(SenderType, name="message_sender_type", create_constraint=True),
        nullable=False,
        default=SenderType.USER,
        comment="Назначение файла: user, ai"
    )
    
    content = Column(
        TEXT, 
        nullable=False,
        comment="Текст сообщения"
    )
    
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        comment="Дата создания записи"
    )
    
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        comment="Дата обновления записи"
    )
