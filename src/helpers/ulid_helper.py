from datetime import date, datetime

from ulid import ULID


def date_from_ulid(ulid_obj: str | ULID) -> date | None:
    result: date | None = None
    try:
        if isinstance(ulid_obj, str):
            ulid_obj = ULID().from_str(ulid_obj.upper())
        timestamp = int(ulid_obj.timestamp * 1000)
        datetime_obj = datetime.fromtimestamp(timestamp / 1000)
        result = datetime_obj.date()
    except ValueError:
        pass
    return result


def ulid_as_str() -> str:
    return str(ULID())


def uuid_as_str() -> str:
    return str(ULID().to_uuid4())
