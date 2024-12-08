from datetime import datetime, timezone

from pydantic import BaseModel, ConfigDict, Field

from db.enums import GDS, Receiver


class GDSReportSchema(BaseModel):
    pnr_id: str = Field(..., min_length=26, max_length=26)
    pnr_file: str = Field(..., min_length=26, max_length=64)
    gds: GDS | None = None
    receiver: Receiver | None = None
    pnr: str | None = Field(None, min_length=1, max_length=16)
    pcc: str | None = Field(None, min_length=1, max_length=16)
    extra_info: dict | None = None
    pnr_emails: dict | None = None
    pnr_passengers: dict | None = None
    received_at: datetime | None = None
    converted_at: datetime | None = None
    routed_at: datetime | None = None
    updated_at: datetime | None = None


class GDSReportSchemaRead(GDSReportSchema):
    id: int
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)


class GDSReportSchemaCreate(GDSReportSchema):
    gds: GDS
    received_at: datetime


class GDSReportSchemaUpdate(GDSReportSchema):
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc).replace(tzinfo=None))
