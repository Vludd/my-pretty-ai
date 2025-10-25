import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base
import app.config as cfg

TABLENAME = "conversations"
FK_users_id = "users.id"

class MConversation(Base):
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
        comment="Public UUID of conversation"
    )
    
    user_id = Column(
        ForeignKey(FK_users_id), 
        nullable=False,
        comment=f"FK {FK_users_id}"
    )
    
    title = Column(
        String(255), 
        nullable=False,
        comment="Title of conversation"
    )
    
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        comment="Created At"
    )
    
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        comment="Updated At"
    )
