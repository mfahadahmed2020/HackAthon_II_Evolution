"""
Database Test Script - Phase 2
Roman Urdu: Yeh script database tables ko test karti hai
"""

import sys
sys.path.insert(0, '.')

from app.database import init_db, verify_database

print("🚀 Phase 2: Database Initialization Test")
print("=" * 50)

# Initialize database
print("\n📊 Initializing database...")
init_db()

# Verify tables
print("\n📋 Verifying tables...")
tables = verify_database()

print("\n✅ Phase 2 Database Setup Complete!")
print("=" * 50)
print(f"📊 Total tables: {len(tables)}")
print(f"📋 Tables: {', '.join(tables)}")
print("\n💡 Next: Start implementing Category routers")
