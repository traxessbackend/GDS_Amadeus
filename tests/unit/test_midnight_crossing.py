import tempfile
import unittest
from datetime import datetime
from pathlib import Path

from helpers.midnight_crossing_helper import read_last_checked_day, write_last_checked_day


class TestDateTimeFunctions(unittest.TestCase):
    def setUp(self):
        # Create a temporary file for testing
        self.temp_file = Path(tempfile.NamedTemporaryFile(delete=False).name)

    def tearDown(self):
        # Clean up temporary file
        if self.temp_file.exists():
            self.temp_file.unlink()

    def test_write_last_checked_day_success(self):
        day = datetime(2024, 11, 28, 15, 30, 0)
        result = write_last_checked_day(self.temp_file, day)
        self.assertTrue(result)
        self.assertEqual(self.temp_file.read_text().strip(), day.strftime("%Y-%m-%d %H:%M:%S"))

    def test_read_last_checked_day_success(self):
        day = datetime(2024, 11, 28, 15, 30, 0)
        self.temp_file.write_text(day.strftime("%Y-%m-%d %H:%M:%S"))
        result = read_last_checked_day(self.temp_file)
        self.assertEqual(result, day)

    def test_read_last_checked_day_file_not_exist(self):
        non_existent_file = Path("non_existent_file.txt")
        result = read_last_checked_day(non_existent_file)
        self.assertIsNone(result)

    def test_read_last_checked_day_invalid_format(self):
        self.temp_file.write_text("invalid_date")
        result = read_last_checked_day(self.temp_file)
        self.assertIsNone(result)

    def test_write_last_checked_day_failure(self):
        invalid_path = Path("/boot/file.txt")
        day = datetime(2024, 11, 28, 15, 30, 0)
        result = write_last_checked_day(invalid_path, day)
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
