from datetime import datetime, timezone

from sqlalchemy import BIGINT, TEXT, DateTime, Enum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

import app.config as cfg
from app.database.base import Base
from app.types.files import FileStatus


class MFile(Base):
    __tablename__ = "files"
    __table_args__ = ({"schema": cfg.DB_SCHEMA} if cfg.DB_SCHEMA != "public" else {})
    
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
        comment="PK"
    )
    
    storage_provider: Mapped[str] = mapped_column(
        String(32), 
        nullable=False, 
        default="local",
        comment="Storage Provider: local, s3, ..."
    )
    
    storage_bucket: Mapped[str] = mapped_column(
        String(128), 
        nullable=True,
        comment="Name of bucket"
    )
    
    storage_key: Mapped[str] = mapped_column(
        TEXT, 
        nullable=False,
        comment="Path to file in storage"
    )
    
    file_name: Mapped[str] = mapped_column(
        TEXT, 
        nullable=False,
        comment="Filename"
    )
    
    mime_type: Mapped[str] = mapped_column(
        String(128), 
        nullable=False,
        comment="MIME-type"
    )
    
    size_bytes: Mapped[int] = mapped_column(
        BIGINT, 
        nullable=False,
        comment="File size in bytes"
    )
    
    checksum_sha256: Mapped[str] = mapped_column(
        TEXT, 
        nullable=False,
        comment="File cheksum"
    )
    
    status: Mapped[FileStatus] = mapped_column(
        Enum(FileStatus, name="file_status", create_constraint=True),
        nullable=False,
        default=FileStatus.ACTIVE,
        comment="File status: active, deleted"
    )
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        comment="Created At"
    )
