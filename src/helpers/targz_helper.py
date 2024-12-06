import logging
import shutil
import tarfile
from datetime import date
from pathlib import Path
from random import randint

from helpers.files_helper import copy_file, rename_existing_file_with_increment

logger = logging.Logger(__name__)


def add_files_to_tar_gz(
    archive_folder: Path,
    tmp_folder: Path,
    files_to_add: list[tuple[Path, date]],
    archive_prefix: str | None = None,
    delete_archived_files: bool = False,
):

    if files_to_add:
        archive_dates = sorted(list(set([file_rec[1] for file_rec in files_to_add])))
        for archive_date in archive_dates:
            files_to_delete: list[Path] = []
            counter_added: int = 0
            try:
                archive_date_str = archive_date.strftime("%Y%m%d")
                # Create a temporary directory for extracting the archive
                temp_dir = tmp_folder / f"temp_tar_{archive_date.strftime('%Y%m%d%H%M%S')}_{randint(0, 9)}"
                temp_dir.mkdir(exist_ok=True, parents=True)
                archive_folder.mkdir(exist_ok=True, parents=True)
                prefix = f"_{archive_prefix}" if archive_prefix else ""
                archive_path = archive_folder / f"{prefix}{archive_date_str}.tar.gz"
                created_subfolders = set()
                # Extract the contents of the existing tar.gz archive
                if archive_path.exists():
                    # with tarfile.open(archive_path, "r:gz") as tar:
                    #     tar.extractall(temp_dir, filter="fully_trusted")
                    with tarfile.open(archive_path, "r:gz") as tar:
                        for member in tar.getmembers():
                            if member.isfile():
                                path_parts = Path(member.name).parts
                                if len(path_parts) < 2:
                                    target_path = temp_dir / member.name
                                else:
                                    adjusted_path = Path(*path_parts[1:])
                                    target_path = temp_dir / adjusted_path
                                    if path_parts[1] not in created_subfolders:
                                        created_subfolders.add(path_parts[1])
                                        target_path.parent.mkdir(parents=True, exist_ok=True)
                                    with tar.extractfile(member) as source, open(target_path, "wb") as dest:
                                        shutil.copyfileobj(source, dest)

                for source_path in filter(lambda rec: rec[1] == archive_date, files_to_add):
                    parent_folder = source_path[0].parents[0].name
                    dest_path = temp_dir / parent_folder
                    if parent_folder not in created_subfolders:
                        dest_path.mkdir(exist_ok=True, parents=True)
                        created_subfolders.add(parent_folder)
                    if copy_file(source_path[0], dest_path):
                        counter_added += 1
                        files_to_delete.append(source_path[0])
                if counter_added:
                    rename_existing_file_with_increment(source_file=archive_path)
                    with tarfile.open(archive_path, "w:gz") as tar:
                        tar.add(temp_dir, arcname=f"./{archive_date_str}")
            except Exception as exc:
                logger.error("Archive error: `%s`", exc)
            else:
                if delete_archived_files:
                    for file in files_to_delete:
                        file.unlink()
            finally:
                # Clean up the temporary directory
                shutil.rmtree(temp_dir, ignore_errors=True)
