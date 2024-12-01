import logging
import re
import shutil
from datetime import date
from pathlib import Path

from helpers.ulid_helper import date_from_ulid

logger = logging.Logger(__name__)


def rename_existing_file_with_increment(source_file: Path) -> Path | None:
    if source_file and source_file.exists() and source_file.is_file():
        counter = 1
        destination_file = source_file
        while True:
            # Create a new filename with an incremented counter
            new_destination = destination_file.with_stem(f"{destination_file.stem}_{counter}")
            if not new_destination.exists():
                destination_file = new_destination
                break
            counter += 1
        # Move the file to the new (or original if no conflict) destination
        source_file.rename(destination_file)
        return destination_file
    return None


def copy_file(source_path: Path, destination_path: Path) -> str | None:
    """
    Copies a file from the source path to the destination path using pathlib.

    :param source: The path to the source file as a Path.
    :param destination: The path to the destination as a Path.
    """
    # Convert source and destination to Path objects
    # Ensure the source file exists
    if not source_path.is_file():
        logger.error("The source file does not exist: `%s`", source_path)
        # raise FileNotFoundError(f"The source file does not exist: {source_path}")
        return None

    # Ensure the destination directory exists
    if not destination_path.parent.exists():
        destination_path.parent.mkdir(parents=True, exist_ok=True)

    # Copy the file
    shutil.copy2(source_path, destination_path)
    logger.info("File copied from `%s` to `%s`", source_path, destination_path)
    return destination_path


def get_ulid_files_list_from_folders(sources: list[Path]) -> list[tuple[Path, date]]:
    # Regex pattern to match ULID, underscore, and date pattern in file names
    pattern = r"^[0-9A-HJKMNP-TV-Z]{10}[0-9A-HJKMNP-TV-Z]{16}_.*"

    # Dictionary to group files by date
    files_with_date = []
    for source_dir in sources:
        if not source_dir.exists():
            continue
        for file in source_dir.iterdir():
            fn = file.name
            if file.is_file() and re.match(pattern, file.name, re.IGNORECASE):
                ulid_str = file.name.split("_", 1)[0]
                try:
                    if not (date_obj := date_from_ulid(ulid_str)):
                        raise ValueError
                except ValueError:
                    continue  # Skip files with invalid date formats
                else:
                    # Add file to the corresponding date group
                    files_with_date.append(
                        (
                            file,
                            date_obj,
                        )
                    )
    return files_with_date
