import sys
import os

# Set path
sys.path.insert(0, r'E:\Python Codes\HackAthon 2\Phase II')
os.chdir(r'E:\Python Codes\HackAthon 2\Phase II')

# Set environment
os.environ['DATABASE_URL'] = 'postgresql://neondb_owner:npg_Ceb1u7LlsctV@ep-holy-band-a73gc162-pooler.ap-southeast-2.aws.neon.tech/neondb?sslmode=require'

print("Step 1: Importing app.main...")
try:
    from app import main
    print("✓ app.main imported successfully")
except Exception as e:
    print(f"✗ Error importing app.main: {e}")
    import traceback
    traceback.print_exc()

print("\nStep 2: Checking app object...")
try:
    from app.main import app
    print(f"✓ app object found: {app}")
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()

print("\nStep 3: Testing database connection...")
try:
    from app.database import engine
    print(f"✓ Database engine created")
    print(f"  URL: {engine.url}")
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()

print("\nDone!")
