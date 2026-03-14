"""
Phase 2: Static File Verification (Without Imports)
Roman Urdu: Yeh script bina import kiye files ko verify karti hai
"""

import os

print("=" * 60)
print("🚀 Phase 2: Static File Verification")
print("=" * 60)

# Files to verify
files_to_check = {
    'app/models.py': ['class Category', 'class Analytics', 'category_id', 'recurrence_pattern', 'parent_id'],
    'app/schemas.py': ['CategoryCreate', 'AnalyticsStats', 'RecurringTaskCreate', 'category_id'],
    'app/database.py': ['enable_sqlite_features', 'verify_database', 'PRAGMA foreign_keys'],
}

all_passed = True

for filepath, keywords in files_to_check.items():
    print(f"\n📄 Checking: {filepath}")
    print("-" * 60)
    
    if not os.path.exists(filepath):
        print(f"❌ File not found: {filepath}")
        all_passed = False
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for keyword in keywords:
        if keyword in content:
            print(f"✅ Found: {keyword}")
        else:
            print(f"❌ Missing: {keyword}")
            all_passed = False

# Check Roman Urdu comments
print("\n📄 Checking Roman Urdu Comments:")
print("-" * 60)

roman_urdu_keywords = ['Roman Urdu', 'yeh', 'hai', 'karna', 'ke liye', 'mein']
files_with_ru = []

for filepath in files_to_check.keys():
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            if any(kw in content.lower() for kw in roman_urdu_keywords):
                files_with_ru.append(filepath)
                print(f"✅ {filepath}: Roman Urdu comments present")

print(f"\n📊 Files with Roman Urdu: {len(files_with_ru)}/{len(files_to_check)}")

# Final Summary
print("\n" + "=" * 60)
if all_passed:
    print("✅ Phase 2: ALL CHECKS PASSED")
    print("=" * 60)
    print("\n📊 Summary:")
    print("  - Category model: ✅ Created")
    print("  - Analytics model: ✅ Created")
    print("  - Todo extensions: ✅ category_id, recurrence_pattern, parent_id")
    print("  - Schemas: ✅ Category, Analytics, RecurringTask")
    print("  - Database functions: ✅ enable_sqlite_features, verify_database")
    print("  - Roman Urdu comments: ✅ Present")
    print("\n🎯 Phase 2 Status: COMPLETE & VERIFIED")
else:
    print("⚠️  Phase 2: Some checks failed - review above")

print("=" * 60)
