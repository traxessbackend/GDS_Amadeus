import random
import shutil
import tarfile
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path

from helpers.targz_helper import add_files_to_tar_gz


def random_date_in_range(start_date, end_date):
    # Convert to datetime objects if they are strings
    if isinstance(start_date, str):
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
    if isinstance(end_date, str):
        end_date = datetime.strptime(end_date, "%Y-%m-%d")

    # Calculate the time difference
    time_delta = end_date - start_date
    random_seconds = random.randint(0, int(time_delta.total_seconds()))

    # Generate random date
    random_date = start_date + timedelta(seconds=random_seconds)
    return random_date.date()


class TestAddFilesToTarGz(unittest.TestCase):
    def setUp(self):
        # Create temporary files and directories for testing
        self.temp_dir = Path(tempfile.mkdtemp())
        self.arch_folder = self.temp_dir / "archive"
        self.arch_folder.mkdir()
        self.files_to_add = []
        self.now = datetime.now()

        # Create an initial tar.gz archive
        self.now_timestamp = self.now.strftime("%Y%m%d")
        self.exists_archive_path = self.arch_folder / f"{self.now_timestamp}.tar.gz"
        self.file_name = f"file_{self.now_timestamp}_0.txt"
        arch_file = self.temp_dir / self.file_name
        arch_file.write_text(" ")
        with tarfile.open(self.exists_archive_path, "w:gz") as tar:
            tar.add(arch_file, arcname=f"./{self.now_timestamp}/{self.file_name}")

        # Create files
        start_date = self.now - timedelta(days=5)
        end_date = self.now - timedelta(days=1)
        ind = 0
        for _ in range(0, random.randint(5, 10)):
            ind += 1
            dt = random_date_in_range(start_date=start_date, end_date=end_date)
            arch_file = self.temp_dir / f"file_{dt.strftime('%Y%m%d')}_{ind}.txt"
            arch_file.touch()
            self.files_to_add.append((arch_file, dt))

        self.file_non_exists = self.temp_dir / "file_non_exists.txt"

    def tearDown(self):
        # Clean up temporary files and directories
        shutil.rmtree(self.temp_dir)

    def test_add_files_to_new_tar_gz_success(self):
        add_file = self.files_to_add[0]
        arch_date = add_file[1]
        arch_date_str = arch_date.strftime("%Y%m%d")
        add_files_to_tar_gz(
            archive_folder=self.arch_folder,
            tmp_folder=self.temp_dir,
            files_to_add=[add_file],
        )
        created_archive = self.arch_folder / f"{arch_date_str}.tar.gz"
        # Verify the new file is in the archive
        with tarfile.open(created_archive, "r:gz") as tar:
            tar_members = [
                file.replace(f"./{arch_date_str}", "").split("_")[1]
                for file in tar.getnames()
                if file.replace(f"./{arch_date_str}", "")
            ]
            self.assertIn(add_file[0].stem.split("_")[1], tar_members)

    def test_add_files_to_tar_gz_no_files_added(self):
        add_files_to_tar_gz(
            archive_folder=self.arch_folder,
            tmp_folder=self.temp_dir,
            files_to_add=[(self.file_non_exists, self.now)],
        )
        # Verify the archive was not modified
        with tarfile.open(self.exists_archive_path, "r:gz") as tar:
            tar_members = [file.split("/")[-1] for file in tar.getnames()]
            self.assertIn(self.file_name, tar_members)
            self.assertNotIn("file_non_exists.txt.txt", tar_members)

    def test_add_files_to_tar_gz_empty_files_to_add(self):
        add_files_to_tar_gz(
            archive_folder=self.exists_archive_path,
            tmp_folder=self.temp_dir,
            files_to_add=[],
        )

        # Verify the archive contents remain unchanged
        with tarfile.open(self.exists_archive_path, "r:gz") as tar:
            tar_members = [file.split("/")[-1] for file in tar.getnames()]
            self.assertIn(self.file_name, tar_members)
            self.assertEqual(len(tar_members), 1)
