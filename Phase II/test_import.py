from app.main import app

print("✓ Import successful - app loaded from app.main")
print(f"✓ App title: {app.title}")
print(f"✓ Routes registered: {len(app.routes)} routes")

# Check routes
for route in app.routes:
    if hasattr(route, 'path'):
        print(f"  - {route.path}")
