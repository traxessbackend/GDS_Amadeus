import shutil
import tarfile
from datetime import date
from pathlib import Path
from random import randint

from helpers.files_helper import copy_file, rename_existing_file_with_increment


def add_files_to_tar_gz(
    archive_folder: Path, tmp_folder: Path, files_to_add: list[tuple[Path, date]], archive_prefix: str | None = None
):
    if files_to_add:
        archive_dates = sorted(list(set([file_rec[1] for file_rec in files_to_add])))
        for archive_date in archive_dates:
            counter_added: int = 0
            try:
                archive_date_str = archive_date.strftime("%Y%m%d")
                # Create a temporary directory for extracting the archive
                temp_dir = tmp_folder / f"temp_tar_{archive_date_str}_{randint(0, 9)}"
                temp_dir.mkdir(exist_ok=True, parents=True)
                archive_folder.mkdir(exist_ok=True, parents=True)
                prefix = f"_{archive_prefix}" if archive_prefix else ""
                archive_path = archive_folder / f"{prefix}{archive_date_str}.tar.gz"
                # Extract the contents of the existing tar.gz archive
                if archive_path.exists():
                    with tarfile.open(archive_path, "r:gz") as tar:
                        tar.extractall(temp_dir, filter="fully_trusted")
                for source_path in filter(lambda rec: rec[1] == archive_date, files_to_add):
                    if copy_file(source_path[0], temp_dir):
                        counter_added += 1
                if counter_added:
                    rename_existing_file_with_increment(source_file=archive_path)
                    with tarfile.open(archive_path, "w:gz") as tar:
                        tar.add(temp_dir, arcname=f"./{archive_date_str}")

            finally:
                # Clean up the temporary directory
                shutil.rmtree(temp_dir, ignore_errors=True)
