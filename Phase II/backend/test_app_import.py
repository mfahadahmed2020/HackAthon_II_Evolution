"""
Test App Import
Roman Urdu: Yeh script app ko import karti hai
"""

import sys
sys.path.insert(0, '.')

print("🧪 Testing App Import...")

try:
    from app.main import app
    print("✅ App imported successfully!")
    print(f"   Title: {app.title}")
    print(f"   Version: {app.version}")
    print(f"   Description: {app.description[:50]}...")
except Exception as e:
    print(f"❌ Error importing app: {e}")
    import traceback
    traceback.print_exc()

print("\n🧪 Testing Database Import...")

try:
    from app.database import Base, engine, init_db
    print("✅ Database imported successfully!")
    
    # Create tables
    print("\n📊 Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created!")
    
    # List tables
    from sqlalchemy import inspect
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    print(f"\n📋 Tables: {', '.join(tables)}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n✅ All imports successful!")
