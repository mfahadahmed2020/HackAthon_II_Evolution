"""
Database initialization script
Creates all tables in the Neon PostgreSQL database
"""

from app.database import create_db_and_tables
from app.config import settings


def init_db():
    """
    Initialize database connection and create tables
    """
    print(f"Connecting to database: {settings.DATABASE_URL[:50]}...")
    
    try:
        create_db_and_tables()
        print("✓ Database tables created successfully!")
        print("\nTables created:")
        print("  - users (for authentication)")
        print("  - tasks (for task management)")
        print("\nDatabase is ready for use!")
        
    except Exception as e:
        print(f"✗ Error creating database tables: {e}")
        print("\nPlease check your DATABASE_URL in .env file")
        raise


if __name__ == "__main__":
    init_db()
