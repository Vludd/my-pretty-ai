from datetime import datetime, timezone
from uuid import UUID as PyUUID
from uuid import uuid4

from sqlalchemy import TEXT, DateTime, Enum, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

import app.config as cfg
from app.database.base import Base
from app.types.messages import SenderType

FK_conversations_id = "conversations.id"
FK_files_id = "files.id"

class MFileMessage(Base):
    __tablename__ = "file_messages"
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
        comment="Public UUID of attached message"
    )
    
    conversation_id: Mapped[int] = mapped_column(
        ForeignKey(FK_conversations_id), 
        nullable=False,
        comment=f"FK {FK_conversations_id}"
    )
    
    file_id: Mapped[int] = mapped_column(
        ForeignKey(FK_files_id), 
        nullable=False,
        comment=f"FK {FK_files_id}"
    )

    sender_type: Mapped[SenderType] = mapped_column(
        Enum(SenderType, name="file_message_sender_type", create_constraint=True),
        nullable=False,
        default=SenderType.USER,
        comment="Sender: user, ai"
    )
    
    content: Mapped[str] = mapped_column(
        TEXT, 
        nullable=True,
        comment="Text of message"
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
