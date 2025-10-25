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
        comment="Первичный ключ записи"
    )
    
    public_id = Column(
        UUID(as_uuid=True),
        unique=True,
        index=True,
        nullable=False,
        default=uuid.uuid4,
        comment="Публичный UUID чата"
    )
    
    user_id = Column(
        ForeignKey(FK_users_id), 
        nullable=False,
        comment=f"Внешний ключ к {FK_users_id}"
    )
    
    title = Column(
        String(255), 
        nullable=False,
        comment="Заголовок чата"
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
