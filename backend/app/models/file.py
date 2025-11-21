from datetime import datetime, timezone

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Enum, TEXT, BIGINT

from app.database.base import Base
import app.config as cfg
from app.types.files import FileStatus

TABLENAME = "files"

class MFile(Base):
    __tablename__ = TABLENAME
    __table_args__ = ({"schema": cfg.DB_SCHEMA} if cfg.DB_SCHEMA != "public" else {})
    
    id = Column(
        Integer,
        primary_key=True,
        index=True,
        comment="PK"
    )
    
    storage_provider = Column(
        String(32), 
        nullable=False, 
        default="local",
        comment="Storage Provider: local, s3, ..."
    )
    
    storage_bucket = Column(
        String(128), 
        nullable=True,
        comment="Name of bucket"
    )
    
    storage_key = Column(
        TEXT, 
        nullable=False,
        comment="Path to file in storage"
    )
    
    file_name = Column(
        TEXT, 
        nullable=False,
        comment="Filename"
    )
    
    mime_type = Column(
        String(128), 
        nullable=False,
        comment="MIME-type"
    )
    
    size_bytes = Column(
        BIGINT, 
        nullable=False,
        comment="File size in bytes"
    )
    
    checksum_sha256 = Column(
        TEXT, 
        nullable=False,
        comment="File cheksum"
    )
    
    status = Column(
        Enum(FileStatus, name="file_status", create_constraint=True),
        nullable=False,
        default=FileStatus.ACTIVE,
        comment="File status: active, deleted"
    )
    
    created_at = Column(DateTime(
        timezone=True),
        default=lambda: datetime.now(timezone.utc),
        comment="Created At"
    )
