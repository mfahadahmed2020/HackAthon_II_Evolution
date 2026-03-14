"""
Test Neon PostgreSQL Connection
"""

import sys
sys.path.insert(0, r'E:\Python Codes\HackAthon 2\Phase II')

from app.config import settings
from app.database import engine, create_db_and_tables
from sqlmodel import SQLModel, Session, select
from datetime import datetime

print("=" * 60)
print("Neon PostgreSQL Connection Test")
print("=" * 60)
print()

# Show database URL (hidden password)
db_url = settings.DATABASE_URL
if "@" in db_url:
    parts = db_url.split("@")
    db_url_display = f"postgresql://***:***@{parts[1]}"
else:
    db_url_display = db_url

print(f"Database: {db_url_display}")
print()

try:
    # Create tables
    print("Creating tables on Neon PostgreSQL...")
    create_db_and_tables()
    print("✓ Tables created successfully!")
    print()
    
    # Test connection
    print("Testing connection...")
    with Session(engine) as session:
        result = session.exec(select(1)).first()
        print(f"✓ Connection working! (Result: {result})")
    
    print()
    print("=" * 60)
    print("✅ SUCCESS! Neon PostgreSQL is connected and ready!")
    print("=" * 60)
    print()
    print("Tables created:")
    print("  - users (authentication)")
    print("  - tasks (task management)")
    print()
    print("Next: Start the server and test API")
    print("  py -3.12 start_server.py")
    print("  Open: http://localhost:8000/docs")
    print()
    
except Exception as e:
    print(f"✗ Error: {str(e)}")
    print()
    print("Troubleshooting:")
    print("1. Check DATABASE_URL in .env file")
    print("2. Verify Neon connection string is correct")
    print("3. Check internet connection")
    print()
