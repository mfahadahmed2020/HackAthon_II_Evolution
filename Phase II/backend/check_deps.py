"""
Dependencies Check Script
Roman Urdu: Yeh script saare dependencies ko verify kart hai
"""

import sys

print("=" * 60)
print("📦 Checking Python Dependencies...")
print("=" * 60)

dependencies = {
    'fastapi': 'FastAPI framework',
    'sqlalchemy': 'Database ORM',
    'pydantic': 'Data validation',
    'uvicorn': 'ASGI server',
    'python_jose': 'JWT tokens',
    'passlib': 'Password hashing',
    'jinja2': 'Templates',
}

all_installed = True

for package, description in dependencies.items():
    try:
        __import__(package.replace('_', '-').split('-')[0])
        print(f"✅ {package:20} - {description}")
    except ImportError:
        print(f"❌ {package:20} - {description} - MISSING")
        all_installed = False

print("=" * 60)

if all_installed:
    print("✅ All dependencies installed!")
    print("\n🚀 Ready to run application...")
else:
    print("\n❌ Some dependencies missing!")
    print("\n💡 Install command:")
    print("   pip install -r requirements.txt")

print("=" * 60)
