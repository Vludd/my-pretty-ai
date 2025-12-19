from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.message import MMessage

from datetime import datetime, timezone
from uuid import UUID as PyUUID
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

import app.config as cfg
from app.database.base import Base

FK_users_id = "users.id"

class MConversation(Base):
    __tablename__ = "conversations"
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
        comment="Public UUID of conversation"
    )
    
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(FK_users_id), 
        nullable=False,
        comment=f"FK {FK_users_id}"
    )
    
    title: Mapped[str] = mapped_column(
        String(255), 
        nullable=False,
        comment="Title of conversation"
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
    
    messages: Mapped[list["MMessage"]] = relationship(
        "MMessage",
        back_populates="conversation",
        cascade="all, delete-orphan",
        passive_deletes=True
    )
