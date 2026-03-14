"""
Start server with correct database connection
Neon PostgreSQL se connect karta hai
"""

import sys
import os

# Add project root to path
sys.path.insert(0, r'E:\Python Codes\HackAthon 2\Phase II')
os.chdir(r'E:\Python Codes\HackAthon 2\Phase II')

# Import and run
import uvicorn
from app.config import settings

print("=" * 60)
print("Starting JWT Authentication and Tasks API")
print("=" * 60)
print()
print(f"Database: {settings.DATABASE_URL[:50]}...")
print(f"CORS Origins: {settings.allowed_origins_list}")
print(f"Debug Mode: {settings.DEBUG}")
print()
print("Starting server on http://localhost:8000")
print("API Docs: http://localhost:8000/docs")
print("=" * 60)
print()

# Start server
uvicorn.run(
    "app.main:app",
    host=settings.HOST,
    port=settings.PORT,
    reload=settings.DEBUG,
)
