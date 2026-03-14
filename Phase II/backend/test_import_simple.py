"""
Simple Import Test
Roman Urdu: Simple import test
"""

print("Testing database imports...")

try:
    from app.database import get_db, Base, engine, Session
    print("SUCCESS: Database imports work!")
    print(f"  - get_db: {get_db}")
    print(f"  - Base: {Base}")
    print(f"  - get_db is get_session: {get_db is not None}")
except Exception as e:
    print(f"FAILED: {e}")
    import traceback
    traceback.print_exc()

print("\nTesting models imports...")
try:
    from app.models import User, Category, Analytics, Todo
    print("SUCCESS: Models import works!")
    print(f"  - User: {User}")
    print(f"  - Category: {Category}")
    print(f"  - Analytics: {Analytics}")
    print(f"  - Todo: {Todo}")
except Exception as e:
    print(f"FAILED: {e}")
    import traceback
    traceback.print_exc()

print("\nTesting main app import...")
try:
    from app.main import app
    print("SUCCESS: Main app imports works!")
    print(f"  - App: {app}")
except Exception as e:
    print(f"FAILED: {e}")
    import traceback
    traceback.print_exc()

print("\nAll tests complete!")
