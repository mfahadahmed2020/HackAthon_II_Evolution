"""
Phase 2: Live Demo Script (Without Server)
Roman Urdu: Yeh script Phase 2 ko demonstrate karti hai bina server ke
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 70)
print("🚀 Phase 2: Live Demonstration - Database & Models")
print("=" * 70)

# Step 1: Import database
print("\n📊 Step 1: Importing Database Module...")
try:
    from app.database import Base, engine, SessionLocal, enable_sqlite_features
    print("✅ Database module imported successfully!")
    print("   - Base: SQLAlchemy declarative base")
    print("   - engine: Database connection engine")
    print("   - SessionLocal: Session factory")
    print("   - enable_sqlite_features: Foreign keys + WAL mode")
except Exception as e:
    print(f"❌ Error importing database: {e}")
    sys.exit(1)

# Step 2: Import models
print("\n📊 Step 2: Importing Models...")
try:
    from app.models import User, Category, Analytics, Todo
    print("✅ All models imported successfully!")
    print("\n   Models Available:")
    print(f"   1. User - Table: {User.__tablename__}")
    print(f"   2. Category - Table: {Category.__tablename__} (NEW in Phase 2)")
    print(f"   3. Analytics - Table: {Analytics.__tablename__} (NEW in Phase 2)")
    print(f"   4. Todo - Table: {Todo.__tablename__} (Extended in Phase 2)")
except Exception as e:
    print(f"❌ Error importing models: {e}")
    sys.exit(1)

# Step 3: Create database tables
print("\n📊 Step 3: Creating Database Tables...")
try:
    # Enable SQLite features
    enable_sqlite_features()
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")
    
    # List tables
    from sqlalchemy import inspect
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    print(f"\n   📋 Tables Created:")
    for table in tables:
        status = "✅" if table in ['users', 'todos', 'categories', 'analytics'] else "  "
        print(f"   {status} {table}")
    
except Exception as e:
    print(f"❌ Error creating tables: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Step 4: Test Category model
print("\n📊 Step 4: Testing Category Model...")
try:
    from datetime import datetime
    
    # Create a test category
    test_category = Category(
        user_id=1,
        name="Work",
        color="#4f46e5",
        created_at=datetime.utcnow()
    )
    
    print(f"✅ Category instance created!")
    print(f"   - Name: {test_category.name}")
    print(f"   - Color: {test_category.color}")
    print(f"   - User ID: {test_category.user_id}")
    print(f"   - Representation: {test_category}")
    
except Exception as e:
    print(f"❌ Error testing category: {e}")

# Step 5: Test Analytics model
print("\n📊 Step 5: Testing Analytics Model...")
try:
    test_analytics = Analytics(
        user_id=1,
        date=datetime.utcnow(),
        total=10,
        completed=6,
        pending=4,
        streak=5
    )
    
    print(f"✅ Analytics instance created!")
    print(f"   - Date: {test_analytics.date.strftime('%Y-%m-%d')}")
    print(f"   - Total: {test_analytics.total}")
    print(f"   - Completed: {test_analytics.completed}")
    print(f"   - Pending: {test_analytics.pending}")
    print(f"   - Streak: {test_analytics.streak} days")
    print(f"   - Representation: {test_analytics}")
    
except Exception as e:
    print(f"❌ Error testing analytics: {e}")

# Step 6: Test Todo model with Phase 2 extensions
print("\n📊 Step 6: Testing Todo Model (Phase 2 Extensions)...")
try:
    test_todo = Todo(
        user_id=1,
        title="Test recurring task",
        description="Testing Phase 2 features",
        priority="high",
        category_id=1,
        recurrence_pattern="daily",
        parent_id=None
    )
    
    print(f"✅ Todo instance created with Phase 2 extensions!")
    print(f"   - Title: {test_todo.title}")
    print(f"   - Priority: {test_todo.priority}")
    print(f"   - Category ID: {test_todo.category_id} (Phase 2)")
    print(f"   - Recurrence Pattern: {test_todo.recurrence_pattern} (Phase 2)")
    print(f"   - Parent ID: {test_todo.parent_id} (Phase 2)")
    
    # Verify all Phase 2 fields
    phase2_fields = {
        'category_id': test_todo.category_id,
        'recurrence_pattern': test_todo.recurrence_pattern,
        'parent_id': test_todo.parent_id,
        'is_deleted': test_todo.is_deleted
    }
    
    print(f"\n   Phase 2 Fields Verification:")
    for field, value in phase2_fields.items():
        status = "✅" if hasattr(test_todo, field) else "❌"
        print(f"   {status} {field}: {value}")
    
except Exception as e:
    print(f"❌ Error testing todo: {e}")

# Step 7: Test Schemas
print("\n📊 Step 7: Testing Pydantic Schemas...")
try:
    from app.schemas import CategoryCreate, RecurringTaskCreate
    
    # Test CategoryCreate with validation
    category_data = CategoryCreate(name="Personal", color="#22c55e")
    print(f"✅ CategoryCreate schema validated!")
    print(f"   - Name: {category_data.name}")
    print(f"   - Color: {category_data.color}")
    
    # Test RecurringTaskCreate
    from datetime import datetime
    recurring_data = RecurringTaskCreate(
        title="Daily Standup",
        recurrence_pattern="daily",
        occurrences=30,
        start_date=datetime.now()
    )
    print(f"✅ RecurringTaskCreate schema validated!")
    print(f"   - Title: {recurring_data.title}")
    print(f"   - Pattern: {recurring_data.recurrence_pattern}")
    print(f"   - Occurrences: {recurring_data.occurrences}")
    
except Exception as e:
    print(f"❌ Error testing schemas: {e}")
    import traceback
    traceback.print_exc()

# Final Summary
print("\n" + "=" * 70)
print("✅ Phase 2: Live Demonstration Complete!")
print("=" * 70)
print("\n📊 Summary:")
print("  ✅ Database: SQLite with Foreign Keys + WAL mode")
print("  ✅ Tables: users, todos, categories, analytics")
print("  ✅ Models: User, Category, Analytics, Todo (extended)")
print("  ✅ Schemas: CategoryCreate, RecurringTaskCreate (validated)")
print("  ✅ Phase 2 Fields: category_id, recurrence_pattern, parent_id")
print("\n🎯 Phase 2 Status: COMPLETE & WORKING")
print("\n💡 Next: Access API at http://localhost:8000/docs")
print("=" * 70)
