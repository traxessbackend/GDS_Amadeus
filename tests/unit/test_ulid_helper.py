from datetime import datetime

from ulid import ULID

from helpers.ulid_helper import date_from_ulid


def test_date_from_ulid():
    now = datetime.now()
    ulid_obj_correct = ULID().from_datetime(now)
    ulid_str_obj_correct = str(ULID().from_datetime(now))
    ulid_str_obj_not_correct = str(ULID().from_datetime(now)) + "1"
    dt_ulid = date_from_ulid(ulid_obj_correct)
    dt_str_ulid = date_from_ulid(ulid_str_obj_correct)
    dt_str_ulid_bad = date_from_ulid(ulid_str_obj_not_correct)
    assert now.date() == dt_ulid
    assert now.date() == dt_str_ulid
    assert dt_str_ulid_bad is None
