"""
Start Server and Open Browser
Roman Urdu: Yeh script server ko start karti hai aur browser open karti hai
"""

import subprocess
import time
import webbrowser
import urllib.request
import sys

print("=" * 70)
print("🚀 Phase 2 Todo App - Starting Server...")
print("=" * 70)

# Start server as subprocess
print("\n📍 Starting Uvicorn server...")
server_process = subprocess.Popen(
    [sys.executable, "-m", "uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"],
    cwd=sys.path[0] if sys.path[0] else '.',
    creationflags=subprocess.CREATE_NEW_CONSOLE
)

print("✅ Server process started!")
print(f"   PID: {server_process.pid}")
print("\n⏳ Waiting for server to be ready...")

# Wait for server to start
max_attempts = 30
for attempt in range(max_attempts):
    try:
        response = urllib.request.urlopen("http://localhost:8000/health", timeout=2)
        if response.status == 200:
            print(f"\n✅ Server is READY! (Attempt {attempt + 1})")
            break
    except:
        print(f"   Attempt {attempt + 1}/{max_attempts}...")
        time.sleep(1)
else:
    print("\n⚠️  Server taking longer than expected...")

# Open browser
print("\n🌐 Opening browser...")
webbrowser.open("http://localhost:8000/docs")
print("✅ Browser opened!")

print("\n" + "=" * 70)
print("✅ Phase 2 Application Running!")
print("=" * 70)
print("\n📍 URLs:")
print("   🏠 Home: http://localhost:8000")
print("   📚 API Docs: http://localhost:8000/docs")
print("   🏥 Health: http://localhost:8000/health")
print("\n💡 Press Ctrl+C in server console to stop")
print("=" * 70)
