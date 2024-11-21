from __future__ import annotations
from enum import Enum

from datetime import datetime

from sqlalchemy import Enum as SQLEnum

from sqlalchemy import (
    Column,
    DateTime,
    String,
    BigInteger,
    func,
    JSON
)
from sqlalchemy.dialects.mssql import CHAR, JSON

from .base import Base
from ..enums import GDS, Receiver


class GDSReports(Base):
    __tablename__ = "gds_reports"
    id: int = Column(
        "id",
        BigInteger,
        autoincrement=True,
        primary_key=True,
    )
    pnr_id: str = Column(CHAR(26),nullable=False)
    gds: Enum | None = Column(SQLEnum(GDS), nullable=True)
    receiver: Enum | None = Column(SQLEnum(Receiver), nullable=True)
    pnr: str = Column(String(16), unique=False, nullable=True)
    pcc: str = Column(String(16), unique=False, nullable=True)
    extra_info: str = Column(JSON, nullable=True)
    pnr_emails: str = Column(JSON, nullable=True)
    pnr_passengers: str = Column(JSON, nullable=True)
    received_at: datetime = Column(DateTime, nullable=False)
    converted_at: datetime = Column(DateTime, nullable=True)
    routed_at: datetime = Column(DateTime, nullable=True)
    updated_at: datetime = Column(DateTime, nullable=True, onupdate=func.now())
    created_at: datetime = Column(DateTime, nullable=False, server_default=func.now())

