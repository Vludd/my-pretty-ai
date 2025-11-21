import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Enum, TEXT, BIGINT
from sqlalchemy.dialects.postgresql import UUID

from app.database.base import Base
import app.config as cfg
from app.types.messages import SenderType

TABLENAME = "file_messages"
FK_conversations_id = "conversations.id"
FK_files_id = "files.id"

class MFileMessage(Base):
    __tablename__ = TABLENAME
    __table_args__ = ({"schema": cfg.DB_SCHEMA} if cfg.DB_SCHEMA != "public" else {})
    
    id = Column(
        Integer,
        primary_key=True,
        index=True,
        comment="PK"
    )
    
    public_id = Column(
        UUID(as_uuid=True),
        unique=True,
        index=True,
        nullable=False,
        default=uuid.uuid4,
        comment="Public UUID of attached message"
    )
    
    conversation_id = Column(
        ForeignKey(FK_conversations_id), 
        nullable=False,
        comment=f"FK {FK_conversations_id}"
    )
    
    file_id = Column(
        ForeignKey(FK_files_id), 
        nullable=False,
        comment=f"FK {FK_files_id}"
    )

    sender_type = Column(
        Enum(SenderType, name="file_message_sender_type", create_constraint=True),
        nullable=False,
        default=SenderType.USER,
        comment="Sender: user, ai"
    )
    
    content = Column(
        TEXT, 
        nullable=True,
        comment="Text of message"
    )
    
    created_at = Column(DateTime(
        timezone=True),
        default=lambda: datetime.now(timezone.utc),
        comment="Created At"
    )
    
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        comment="Updated At"
    )
