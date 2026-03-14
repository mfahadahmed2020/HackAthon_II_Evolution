"""
Database connection and session management
Uses Neon Serverless PostgreSQL with SQLModel
"""

from sqlmodel import SQLModel, create_engine, Session
from typing import Generator
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

# Create engine with connection pooling
# Neon serverless handles connection pooling automatically
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Set to True for SQL debugging
    pool_pre_ping=True,  # Enable connection health checks
    pool_size=10,  # Connection pool size
    max_overflow=20,  # Max connections beyond pool_size
)


def create_db_and_tables() -> None:
    """
    Create all database tables
    Call this on application startup
    """
    from backend.src.models.user import User  # Import models to register them
    
    # Create extensions (requires superuser privileges on Neon)
    # Note: Run this manually or via migration script:
    # CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
    
    # Create all tables
    SQLModel.metadata.create_all(engine)
    print("Database tables created successfully")


def get_session() -> Generator[Session, None, None]:
    """
    Dependency that provides a database session
    Usage: session: Session = Depends(get_session)
    """
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()


def get_engine():
    """
    Get the database engine directly
    Use for raw SQL queries
    """
    return engine
