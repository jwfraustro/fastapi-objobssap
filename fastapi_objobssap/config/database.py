"""This module contains the database configuration for the application."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fastapi_objobssap.config.settings import get_settings
from contextlib import contextmanager

settings = get_settings()

engine = create_engine(
    url=settings.POSTGRES_DATABASE_URL,
    pool_pre_ping=True,
    pool_size=100,  # The size of the connection pool
    max_overflow=50,  # The maximum number of connections that can be opened beyond the pool size. Set to -1 for no limit.
)
SessionLocal = sessionmaker(bind=engine)

@contextmanager
def get_db():
    """This function starts a db session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
