from datetime import datetime, timezone
from uuid import UUID as PyUUID
from uuid import uuid4

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

import app.config as cfg
from app.database.base import Base


class MUser(Base):
    __tablename__ = "users"
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
        comment="Public UUID of user"
    )
    
    username: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
        comment="Username"
    )
    
    email: Mapped[str] = mapped_column(
        String(255), 
        nullable=False,
        unique=True,
        index=True,
        comment="User Email"
    )
    
    password_hash: Mapped[str] = mapped_column(
        String(255), 
        nullable=True, 
        default=None,
        comment="User password (hashed)"
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
    
    last_login_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=None,
        comment="Last Login At"
    )
