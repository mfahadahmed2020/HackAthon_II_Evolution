"""
Force reload config and test Neon connection
"""
import os
import sys

# Set environment variable BEFORE importing config
os.environ['DATABASE_URL'] = 'postgresql://neondb_owner:npg_Ceb1u7LlsctV@ep-holy-band-a73gc162-pooler.ap-southeast-2.aws.neon.tech/neondb?sslmode=require'

sys.path.insert(0, r'E:\Python Codes\HackAthon 2\Phase II')

# Now import config
from app.config import Settings

settings = Settings()

print("=" * 60)
print("Database Configuration")
print("=" * 60)
print(f"Database URL: {settings.DATABASE_URL[:60]}...")
print(f"Database Type: {'Neon PostgreSQL' if 'neon' in settings.DATABASE_URL else 'SQLite'}")
print(f"CORS Origins: {settings.allowed_origins_list}")
print("=" * 60)
