import logging
from contextlib import contextmanager
from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from settings import settings

logger = logging.getLogger(__name__)

engine = create_engine(settings.DATABASE_URL, echo=settings.ECHO_SQL, pool_size=10, max_overflow=20)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


@contextmanager
def get_session():
    session = SessionLocal()
    try:
        yield session
        session.commit()  # Commit the transaction if no exception occurs
    except Exception as e:
        session.rollback()  # Roll back on exception
        raise  # Re-raise the exception
    finally:
        session.close()  # Ensure the session is closed
