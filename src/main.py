from datetime import datetime
from pathlib import Path

from gds.amadeus.amadeus_api import AmadeusAPI
from helpers.files_helper import get_ulid_files_list_from_folders
from helpers.midnight_crossing_helper import (
    datetime_format,
    days_difference,
    read_last_checked_day,
    write_last_checked_day,
)
from helpers.targz_helper import add_files_to_tar_gz
from logger import init_logger
from settings import settings

init_logger()


def main() -> None:
    now = datetime.now()
    last_run_file: Path = settings.WORKDIR / "last_run.datetime"
    last_checked_day = read_last_checked_day(filename=last_run_file)
    if days_difference(date1=now, date2=last_checked_day):
        archive_filename = settings.WORKDIR / f"archive/{last_checked_day.strftime(datetime_format)}.tar.gz"
        tmp_folder = settings.WORKDIR / "tmp"

        files_to_add = get_ulid_files_list_from_folders(
            sources=[settings.WORKDIR / "session", settings.WORKDIR / "current_pnr", settings]
        )
        add_files_to_tar_gz(
            archive_path=archive_filename, tmp_folder=tmp_folder, files_to_add=[rec[0] for rec in files_to_add]
        )
    amadeus = AmadeusAPI(
        username=settings.USER,
        password=settings.PASSWORD,
        officeid=settings.OFFICEID,
        pseudocitycode=settings.PSEUDOCITYCODE,
        workdir=settings.WORKDIR,
        notify_slack=bool(settings.SLACK_WEBHOOK_URL),
        queue_alert_level_accessible=settings.QUEUE_ALERT_LEVEL_ACCESIBLE,
        queue_alert_total_accessible_ratio=settings.QUEUE_ALERT_TOTAL_RATIO,
    )
    amadeus.launch_work_cycle(queue_ids=settings.QUEUE_IDS)
    write_last_checked_day(filename=files_to_add, day=now)


if __name__ == "__main__":
    main()
