import logging
from typing import Iterator

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from settings import settings

logger = logging.getLogger(__name__)

engine = create_engine(settings.DATABASE_URL, echo=settings.ECHO_SQL, pool_size=10, max_overflow=20)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


def get_session() -> Iterator[sessionmaker]:
    try:
        yield SessionLocal
    except SQLAlchemyError as e:
        logger.exception(e)
