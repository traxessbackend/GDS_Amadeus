from datetime import date, datetime

from ulid import ULID


def date_from_ulid(ulid_obj: str | ULID) -> date | None:
    result: date | None = None
    try:
        if isinstance(ulid_obj, str):
            ulid_obj = ULID(ulid_obj)

        timestamp = int(ulid_obj.timestamp * 1000)
        datetime_obj = datetime.fromtimestamp(timestamp / 1000)
        result = datetime_obj.date()
    except:
        pass
    return result


def ulid_as_str() -> str:
    return str(ULID().to_uuid4())
