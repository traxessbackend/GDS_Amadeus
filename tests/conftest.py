import sys
from datetime import UTC, datetime
from pathlib import Path

import pytest
from pytest_mock import MockerFixture

# Add the src directory to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent / "./src"))

from settings import settings


@pytest.fixture
def test_fixture() -> None:
    return None


class MockDateTime(datetime):
    """Mock datetime.datetime.now() to return a constant datetime."""

    @classmethod
    def now(cls):
        return datetime(2023, 1, 1, tzinfo=UTC)


@pytest.fixture
def mock_settings(mocker: MockerFixture):
    return mocker.patch("settings.settings")
