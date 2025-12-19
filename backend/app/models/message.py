from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.conversation import MConversation

from datetime import datetime, timezone
from uuid import UUID as PyUUID
from uuid import uuid4

from sqlalchemy import TEXT, Boolean, DateTime, Enum, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

import app.config as cfg
from app.database.base import Base
from app.types.messages import SenderType

FK_conversations_id = "conversations.id"

class MMessage(Base):
    __tablename__ = "messages"
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
        comment="Public UUID of message"
    )
    
    conversation_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(FK_conversations_id), 
        nullable=False,
        comment=f"FK {FK_conversations_id}"
    )
    
    sender_type: Mapped[SenderType] = mapped_column(
        Enum(SenderType, name="message_sender_type", create_constraint=True),
        nullable=False,
        default=SenderType.USER,
        comment="Sender: user, ai"
    )
    
    content: Mapped[str] = mapped_column(
        TEXT, 
        nullable=False,
        comment="Text of message"
    )
    
    deleted: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        comment="Soft delete flag"
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
    
    conversation: Mapped["MConversation"] = relationship(
        "MConversation",
        back_populates="messages"
    )
