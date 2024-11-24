import shutil
import tarfile
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from helpers.targz_helper import add_files_to_tar_gz


class TestAddFilesToTarGz(unittest.TestCase):
    def setUp(self):
        # Create temporary files and directories for testing
        self.temp_dir = Path(tempfile.mkdtemp())
        self.archive_path = self.temp_dir / "test_archive.tar.gz"
        self.tmp_folder = self.temp_dir / "tmp"
        self.tmp_folder.mkdir()

        # Create an initial tar.gz archive
        with tarfile.open(self.archive_path, "w:gz") as tar:
            dummy_file = self.temp_dir / "dummy.txt"
            dummy_file.write_text("dummy content")
            tar.add(dummy_file, arcname="dummy.txt")

        # Files to add
        self.file_exists = self.temp_dir / "file_exists.txt"
        self.file_exists.write_text("file to add content")
        self.file_non_exists = self.temp_dir / "file_non_exists.txt"

    def tearDown(self):
        # Clean up temporary files and directories
        shutil.rmtree(self.temp_dir)

    def test_add_files_to_tar_gz_success(self):
        add_files_to_tar_gz(
            archive_path=self.archive_path,
            tmp_folder=self.tmp_folder,
            files_to_add=[self.file_exists],
        )

        # Verify the new file is in the archive
        with tarfile.open(self.archive_path, "r:gz") as tar:
            tar_members = [file.split("./")[-1] for file in tar.getnames()]
            self.assertIn("dummy.txt", tar_members)
            self.assertIn("file_exists.txt", tar_members)

    def test_add_files_to_tar_gz_no_files_added(self):
        add_files_to_tar_gz(
            archive_path=self.archive_path,
            tmp_folder=self.tmp_folder,
            files_to_add=[self.file_non_exists],
        )

        # Verify the archive was not modified
        with tarfile.open(self.archive_path, "r:gz") as tar:
            tar_members = [file.split("./")[-1] for file in tar.getnames()]
            self.assertIn("dummy.txt", tar_members)
            self.assertNotIn("file_non_exists.txt.txt", tar_members)

    def test_add_files_to_tar_gz_empty_files_to_add(self):
        add_files_to_tar_gz(
            archive_path=self.archive_path,
            tmp_folder=self.tmp_folder,
            files_to_add=[],
        )

        # Verify the archive contents remain unchanged
        with tarfile.open(self.archive_path, "r:gz") as tar:
            tar_members = tar.getnames()
            self.assertIn("dummy.txt", tar_members)
            self.assertEqual(len(tar_members), 1)

    def test_add_files_to_tar_gz_invalid_archive(self):
        invalid_archive = self.tmp_folder / "invalid_archive.tar.gz"
        invalid_archive.write_text("not a valid tar.gz file")

        with self.assertRaises(tarfile.ReadError):
            add_files_to_tar_gz(
                archive_path=invalid_archive,
                tmp_folder=self.tmp_folder,
                files_to_add=[self.file_exists],
            )
