import tempfile
from datetime import date
from pathlib import Path

import pytest
from ulid import ULID

from helpers.files_helper import copy_file, get_ulid_files_list_from_folders, rename_existing_file_with_increment


def test_rename_existing_file_with_increment():
    # Create a temporary directory to hold test files
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Case 1: File does not exist
        non_existent_file = temp_path / "nonexistent.txt"
        assert rename_existing_file_with_increment(non_existent_file) is None

        # Case 2: File exists and no conflicts
        existing_file = temp_path / "example.txt"
        renamed_file = temp_path / "example_1.txt"
        existing_file.touch()  # Create the file
        result = rename_existing_file_with_increment(existing_file)
        assert result == renamed_file
        assert result.exists()
        assert not existing_file.exists()

        # Case 3: File not exists
        conflict_file_1 = temp_path / "example.txt"
        # conflict_file_1.touch()  # Create a conflicting file

        new_file = rename_existing_file_with_increment(conflict_file_1)
        assert new_file is None

        # Case 4: Multiple conflicts
        existing_file = temp_path / "example.txt"
        existing_file.touch()  # Create the file
        conflict_file_2 = temp_path / "example_1.txt"
        conflict_file_2.touch()
        conflict_file_3 = temp_path / "example_2.txt"
        conflict_file_3.touch()

        final_file = rename_existing_file_with_increment(existing_file)
        assert final_file.name == "example_3.txt"
        assert final_file.exists()


def test_copy_file():
    # Create a temporary directory to hold test files
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Case 1: Source file does not exist
        non_existent_file = temp_path / "nonexistent.txt"
        destination_file = temp_path / "copy_nonexistent.txt"
        result = copy_file(non_existent_file, destination_file)
        assert result is None  # Function should return None
        assert not destination_file.exists()

        # Case 2: Source file exists, and destination path is valid
        source_file = temp_path / "source.txt"
        source_file.write_text("This is a test file.")  # Create and write to the source file
        destination_file = temp_path / "destination.txt"

        result = copy_file(source_file, destination_file)
        assert result == destination_file  # The returned path should match the destination
        assert destination_file.exists()  # The destination file should exist
        assert destination_file.read_text() == "This is a test file."  # Content should match

        # Case 3: Destination directory does not exist
        new_directory = temp_path / "new_directory"
        destination_in_new_dir = new_directory / "nested_destination.txt"

        result = copy_file(source_file, destination_in_new_dir)
        assert result == destination_in_new_dir  # The returned path should match
        assert destination_in_new_dir.exists()  # The destination file should exist
        assert destination_in_new_dir.read_text() == "This is a test file."  # Content should match
        assert new_directory.exists()  # The directory should be created

        # Case 4: Overwriting an existing destination file
        existing_file = temp_path / "existing_file.txt"
        existing_file.write_text("Old content.")  # Create a destination file with old content

        result = copy_file(source_file, existing_file)
        assert result == existing_file  # The returned path should match
        assert existing_file.exists()  # The file should still exist
        assert existing_file.read_text() == "This is a test file."  # Content should be updated


def test_get_ulid_files_list_from_folders():
    # Use a temporary directory to simulate input folders
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Create source folders
        folder1 = temp_path / "folder1"
        folder1.mkdir()
        folder2 = temp_path / "folder2"
        folder2.mkdir()

        # Create files in folder1
        (folder1 / f"{str(ULID())}_1.txt").touch()
        (folder1 / f"{str(ULID())}_2.log").touch()
        (folder1 / "invalid_file.txt").touch()

        # Create files in folder2
        (folder2 / f"{str(ULID())}_1").touch()
        (folder2 / "random_file_123.txt").touch()

        now = date.today()
        result = get_ulid_files_list_from_folders([folder1, folder2])

        # Verify the output dictionary
        assert len(result) == 3  # Two unique dates
        assert now in [rec[1] for rec in result]
