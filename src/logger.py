import logging
import os
import sys
from enum import StrEnum
from logging.handlers import TimedRotatingFileHandler

import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration
from slack_logger import SlackFormatter, SlackHandler, SlackLogFilter

from settings import settings

log_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")


class LogDestinations(StrEnum):
    FILE = "file"
    CONSOLE = "console"
    SENTRY = "sentry"
    SLACK = "slack"


log_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")


def init_logger(app_name: str | None = None, log_level: str | None = None) -> logging.Logger:
    log_destinations = [destination.lower() for destination in settings.LOG_DESTINATIONS]

    if log_level is None:
        log_level = settings.LOG_LEVEL.upper()

    if LogDestinations.SENTRY in log_destinations:
        init_sentry_logger()

    logger = logging.getLogger(app_name)
    logger.setLevel(log_level)

    # Clear any previously attached handlers
    logger.handlers.clear()

    # Set the logging destination
    if LogDestinations.FILE in log_destinations:
        logger.addHandler(_get_file_rotating_handler())
    if LogDestinations.CONSOLE in log_destinations:
        logger.addHandler(_get_stream_handler())
    if LogDestinations.SLACK in log_destinations:
        logger.addHandler(init_slack_logger())

    return logger


def _traces_sampler(ctx):
    if ctx["parent_sampled"] is not None:
        # If this transaction has a parent, we usually want to sample it
        # if and only if its parent was sampled.
        return ctx["parent_sampled"]
    op = ctx["transaction_context"]["op"]
    if "wsgi_environ" in ctx:
        # Get the URL for WSGI requests
        url = ctx["wsgi_environ"].get("PATH_INFO", "")
    elif "asgi_scope" in ctx:
        # Get the URL for ASGI requests
        url = ctx["asgi_scope"].get("path", "")
    else:
        # Other kinds of transactions don't have a URL
        url = ""
    if op == "http.server":
        # Conditions only relevant to operation "http.server"
        if url[-6:] == "health":
            return 0  # Don't trace any of these transactions
    return 0.5  # Sample other transactions at 50%


def init_slack_logger() -> SlackHandler:
    sh = SlackHandler(settings.SLACK_WEB_HOOCK_URL)
    sh.setFormatter(SlackFormatter())
    sh.addFilter(SlackLogFilter())
    return sh


def init_sentry_logger():
    if settings.SENTRY_DSN is None:
        raise ValueError("SENTRY_DSN is not set")

    sentry_logging = LoggingIntegration(
        level=logging.INFO, event_level=logging.ERROR  # Capture info and above as breadcrumbs  # Send errors as events
    )

    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        integrations=[
            sentry_logging,
        ],
        traces_sampler=_traces_sampler,
        profiles_sample_rate=0.5,  # Sample profiles at 50%
        environment=os.environ["APP_ENV"],
        # Collect personal data
        send_default_pii=True,
    )


def _get_file_rotating_handler():
    _create_logs_dir_if_not_exists()

    handler = TimedRotatingFileHandler("logs/backend.log", when="midnight", backupCount=3)

    handler.setFormatter(log_format)
    return handler


def _get_stream_handler():
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(log_format)
    return handler


def _create_logs_dir_if_not_exists():
    if not os.path.exists("logs"):
        os.makedirs("logs")


def get_uvicorn_log_config() -> dict:
    access_log_level = settings.UVICORN_ACCESS_LOG_LEVEL.upper()
    error_log_level = settings.UVICORN_ERROR_LOG_LEVEL.upper()
    handlers_list = settings.UVICORN_LOG_HANDLERS

    available_handlers = {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "uvicorn_default",
        },
        "file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": "logs/uvicorn.log",
            "when": "midnight",
            "backupCount": 3,
            "formatter": "with_time",
        },
    }

    if LogDestinations.FILE in handlers_list:
        _create_logs_dir_if_not_exists()

    LOGGING_CONFIG = {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {handler: available_handlers[handler] for handler in handlers_list},
        "formatters": {
            "uvicorn_default": {
                "()": "uvicorn.logging.DefaultFormatter",
                "fmt": "%(levelprefix)s %(message)s",
                "use_colors": True,
            },
            "with_time": {
                "format": "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "loggers": {
            "uvicorn": {
                "handlers": handlers_list,
                "level": error_log_level,
                "propagate": False,  # Prevents double logging
            },
            "uvicorn.error": {
                "handlers": handlers_list,
                "level": error_log_level,
                "propagate": False,  # Prevents double logging
            },
            "uvicorn.access": {
                "handlers": handlers_list,
                "level": access_log_level,
                "propagate": False,  # Prevents double logging
            },
        },
    }
    return LOGGING_CONFIG
