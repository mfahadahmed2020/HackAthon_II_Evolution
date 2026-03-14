"""
Start server and show all errors
Updated for backend/ folder structure
"""
import sys
import os

# Set path to backend directory
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)
os.chdir(backend_dir)

# Set environment
os.environ['DATABASE_URL'] = 'postgresql://neondb_owner:npg_Ceb1u7LlsctV@ep-holy-band-a73gc162-pooler.ap-southeast-2.aws.neon.tech/neondb?sslmode=require'

print("=" * 60)
print("Starting FastAPI Server")
print("=" * 60)
print(f"Database: Neon PostgreSQL")
print(f"URL: http://localhost:8000")
print(f"Docs: http://localhost:8000/docs")
print("=" * 60)
print()

try:
    import uvicorn
    from app.main import app
    
    print("✓ App loaded successfully")
    print()
    print("Starting server...")
    print()
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    )
    
except Exception as e:
    print(f"✗ ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
