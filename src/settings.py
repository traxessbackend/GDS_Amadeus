import logging
import os
from decimal import Decimal
from pathlib import Path
from typing import ClassVar

from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)


def get_current_env() -> str:
    try:
        return os.environ["APP_ENV"]
    except KeyError:
        return "development"


def _get_env_file() -> Path:
    env = get_current_env()
    logger.warning("Loading `%s` environment", env)
    return Path(__file__).parent / f"config/{env}.env"


class Settings(BaseSettings):
    PROJECT_NAME: str

    LOG_LEVEL: str = "INFO"
    LOG_DESTINATIONS: list = ["console"]
    SENTRY_DSN: str | None = None

    DATABASE_URL: str | None = None

    ECHO_SQL: bool = False

    USER: str
    PASSWORD: str
    OFFICEID: str
    PSEUDOCITYCODE: str

    WORKDIR: str

    SLACK_WEBHOOK_URL: str | None = None
    QUEUE_ALERT_TOTAL_RATIO: int = 100
    QUEUE_ALERT_LEVEL_ACCESIBLE: Decimal = Decimal(2.0)

    QUEUE_IDS: list[int]
    ENABLE_DELETE_PNR_FROM_QUEUE: bool = False

    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        env_file=_get_env_file(),
    )


settings = Settings()
