from __future__ import annotations

from datetime import datetime
from enum import Enum

from sqlalchemy import JSON, BigInteger, Column, DateTime
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import String, func
from sqlalchemy.dialects.mssql import CHAR, JSON

from ..enums import GDS, Receiver
from .base import Base


class GDSReports(Base):
    __tablename__ = "gds_reports"
    id: int = Column(
        "id",
        BigInteger,
        autoincrement=True,
        primary_key=True,
    )
    pnr_id: str = Column(CHAR(26), nullable=False)
    gds: Enum | None = Column(SQLEnum(GDS), nullable=True)
    receiver: Enum | None = Column(SQLEnum(Receiver), nullable=True)
    pnr_file: str = Column(String(64), unique=False, nullable=False)
    pnr: str = Column(String(16), unique=False, nullable=True)
    pcc: str = Column(String(16), unique=False, nullable=True)
    extra_info: str = Column(JSON, nullable=True)
    pnr_emails: str = Column(JSON, nullable=True)
    pnr_passengers: str = Column(JSON, nullable=True)
    received_at: datetime = Column(DateTime(timezone=True), nullable=False)
    converted_at: datetime = Column(DateTime(timezone=True), nullable=True)
    routed_at: datetime = Column(DateTime(timezone=True), nullable=True)
    created_at: datetime = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: datetime = Column(
        DateTime(timezone=True), nullable=True, server_default=func.now(), onupdate=func.now()
    )
