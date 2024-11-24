import os
import shutil
import tarfile
from datetime import datetime
from pathlib import Path
from random import randint

from helpers.files_helper import copy_file, rename_existing_file_with_increment


def add_files_to_tar_gz(archive_path: Path, tmp_folder: Path, files_to_add: list[Path]):
    # Create a temporary directory for extracting the archive
    temp_dir = tmp_folder / f"temp_tar_{datetime.now().strftime('%Y%m%d%H%M%S')}_{randint(0, 9)}"
    os.makedirs(temp_dir, exist_ok=True)
    counter_added: int = 0
    if files_to_add:
        try:
            # Extract the contents of the existing tar.gz archive
            with tarfile.open(archive_path, "r:gz") as tar:
                tar.extractall(temp_dir)

            for source_path in files_to_add:
                if copy_file(source_path, temp_dir):
                    counter_added += 1
            if counter_added:
                rename_existing_file_with_increment(source_file=archive_path)
                with tarfile.open(archive_path, "w:gz") as tar:
                    tar.add(temp_dir, arcname=".")

        finally:
            # Clean up the temporary directory
            shutil.rmtree(temp_dir)
