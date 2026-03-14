"""
Database Connection Test Script
Neon PostgreSQL connection verify karne ke liye
"""

import sys
from app.database import engine, create_db_and_tables
from app.config import settings
from sqlmodel import SQLModel, Session, select
from datetime import datetime


def test_connection():
    """
    Test database connection
    """
    print("=" * 60)
    print("Database Connection Test")
    print("=" * 60)
    print()
    
    # Show connection info (without password)
    db_url_display = settings.DATABASE_URL
    if "@" in db_url_display:
        # Hide password for security
        parts = db_url_display.split("@")
        db_url_display = f"postgresql://***:***@{parts[1]}"
    
    print(f"Database URL: {db_url_display}")
    print(f"Database Type: Neon PostgreSQL")
    print()
    
    try:
        # Test connection
        print("Testing connection...")
        with Session(engine) as session:
            result = session.exec(select(1)).first()
            print(f"✓ Connection successful! (Result: {result})")
        
        print()
        print("✓ Database connection is working!")
        print()
        
        return True
        
    except Exception as e:
        print(f"✗ Connection failed!")
        print(f"Error: {str(e)}")
        print()
        print("Troubleshooting tips:")
        print("1. Check DATABASE_URL in .env file")
        print("2. Verify your Neon connection string is correct")
        print("3. Check internet connection")
        print("4. Ensure Neon project allows connections")
        print()
        return False


def test_tables():
    """
    Test table creation
    """
    print("=" * 60)
    print("Table Creation Test")
    print("=" * 60)
    print()
    
    try:
        print("Creating tables (if not exists)...")
        create_db_and_tables()
        print("✓ Tables created successfully!")
        print()
        print("Tables:")
        print("  - users (authentication)")
        print("  - tasks (task management)")
        print()
        
        return True
        
    except Exception as e:
        print(f"✗ Table creation failed!")
        print(f"Error: {str(e)}")
        print()
        return False


def main():
    """
    Main test function
    """
    print()
    print("╔══════════════════════════════════════════════════════════╗")
    print("║  Neon PostgreSQL Connection Test                         ║")
    print("║  SQLite se PostgreSQL migration verification             ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print()
    
    # Test 1: Connection
    connection_ok = test_connection()
    
    if not connection_ok:
        print("Connection test failed. Fix the issues above and try again.")
        sys.exit(1)
    
    # Test 2: Tables
    tables_ok = test_tables()
    
    if not tables_ok:
        print("Table creation failed. Check permissions and try again.")
        sys.exit(1)
    
    # Success
    print("=" * 60)
    print("✅ All Tests Passed!")
    print("=" * 60)
    print()
    print("Your backend is now connected to Neon PostgreSQL!")
    print()
    print("Next steps:")
    print("1. Start the server: uvicorn app.main:app --reload")
    print("2. Open browser: http://localhost:8000/docs")
    print("3. Test API endpoints")
    print("4. Connect Next.js frontend (http://localhost:3000)")
    print()
    print("CORS is enabled for: http://localhost:3000")
    print()


if __name__ == "__main__":
    main()
