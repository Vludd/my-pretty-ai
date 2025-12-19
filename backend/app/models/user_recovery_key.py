from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

import app.config as cfg
from app.database.base import Base

FK_users_id = "users.id"

class MUserRecoveryKey(Base):
    __tablename__ = "user_recovery_keys"
    __table_args__ = ({"schema": cfg.DB_SCHEMA} if cfg.DB_SCHEMA != "public" else {})
    
    id: Mapped[int] = mapped_column(
        Integer, 
        primary_key=True, 
        index=True,
        comment="PK"
    )
    
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(FK_users_id), 
        nullable=True,
        comment=f"FK {FK_users_id}"
    )
    
    key_hash: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        comment="Key hash"
    )
    
    used: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        comment="Key is used?"
    )
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        comment="Created At"
    )
    
    used_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        comment="Used At"
    )
