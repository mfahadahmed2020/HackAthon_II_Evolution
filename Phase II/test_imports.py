"""
Import Verification Script
Roman Urdu: Imports verify karna ke fix kaam kar raha hai
"""

import sys
import os

# Add backend to path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

print("=" * 60)
print("IMPORT VERIFICATION TEST")
print("=" * 60)

# Test 1: Database imports
print("\n1. Testing database imports...")
try:
    from app.database import get_db, Base, engine, Session, get_session, create_db_and_tables
    print("   ✓ get_db imported successfully")
    print("   ✓ Base imported successfully")
    print("   ✓ engine imported successfully")
    print("   ✓ Session imported successfully")
    print("   ✓ get_session imported successfully")
    print("   ✓ create_db_and_tables imported successfully")
    print(f"   ✓ get_db is alias for get_session: {get_db is get_session}")
except Exception as e:
    print(f"   ✗ Database import failed: {e}")
    sys.exit(1)

# Test 2: Models imports
print("\n2. Testing models imports...")
try:
    from app.models import User, Category, Analytics, Todo
    print("   ✓ User model imported successfully")
    print("   ✓ Category model imported successfully")
    print("   ✓ Analytics model imported successfully")
    print("   ✓ Todo model imported successfully")
except Exception as e:
    print(f"   ✗ Models import failed: {e}")
    sys.exit(1)

# Test 3: Router imports
print("\n3. Testing router imports...")
try:
    from app.routers import auth, todos, categories, analytics, users
    print("   ✓ auth router imported successfully")
    print("   ✓ todos router imported successfully")
    print("   ✓ categories router imported successfully")
    print("   ✓ analytics router imported successfully")
    print("   ✓ users router imported successfully")
except Exception as e:
    print(f"   ✗ Router import failed: {e}")
    sys.exit(1)

# Test 4: Main app import
print("\n4. Testing main app import...")
try:
    from app.main import app
    print("   ✓ Main app imported successfully")
    print(f"   ✓ App title: {app.title}")
except Exception as e:
    print(f"   ✗ Main app import failed: {e}")
    sys.exit(1)

# Test 5: Auth module
print("\n5. Testing auth module...")
try:
    from app.auth import get_current_user, create_access_token
    print("   ✓ get_current_user imported successfully")
    print("   ✓ create_access_token imported successfully")
except Exception as e:
    print(f"   ✗ Auth module import failed: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("✅ ALL IMPORTS VERIFIED SUCCESSFULLY!")
print("=" * 60)
print("\nNext step: Start server with 'py -3.12 -m uvicorn app.main:app --reload'")
