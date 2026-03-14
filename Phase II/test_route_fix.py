import fastapi
print(f"FastAPI version: {fastapi.__version__}")

from app.main import app
print(f"✓ App loaded successfully")
print(f"App title: {app.title}")
print(f"Routes: {len(app.routes)}")

# Check for /api prefix
for route in app.routes:
    if hasattr(route, 'path') and route.path.startswith('/api'):
        print(f"  ✓ API Route: {route.path}")
