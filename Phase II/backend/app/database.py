"""
Database configuration using SQLModel
Connects to Neon PostgreSQL with connection pooling
SQLite se PostgreSQL (Neon) par shift kiya gaya hai
"""

from sqlmodel import SQLModel, create_engine, Session
from typing import Generator

from app.config import settings


# Create database engine with connection pooling for Neon PostgreSQL
# pool_pre_ping=True handles Neon connection drops automatically
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # Handle Neon connection drops
    pool_size=10,
    max_overflow=20,
    echo=settings.DEBUG,  # Log SQL queries in debug mode
)


# Phase 1 Import Fix: Export Base for models
# Roman Urdu: Models ke liye Base class export karna
Base = SQLModel.metadata


def create_db_and_tables() -> None:
    """
    Create all database tables
    Call this on application startup
    Neon PostgreSQL par tables create karta hai
    """
    create_db_and_tables_from_metadata()


def create_db_and_tables_from_metadata() -> None:
    """
    Create all database tables from metadata
    Roman Urdu: SQLModel metadata se tables create karna
    """
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """
    Dependency for getting database session
    Usage: session: Session = Depends(get_session)
    """
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()


# Phase 1 Import Fix: Export get_db for backward compatibility
# Roman Urdu: Routers ke liye get_db alias (get_session ka alias)
get_db = get_session


# Export all public symbols
# Roman Urdu: Saare public symbols export karna
__all__ = [
    'engine',
    'Base',
    'Session',
    'SQLModel',
    'create_db_and_tables',
    'create_db_and_tables_from_metadata',
    'get_session',
    'get_db',
]
