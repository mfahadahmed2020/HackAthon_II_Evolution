"""
Test Server Connection
Roman Urdu: Yeh script server ko test karti hai
"""

import urllib.request
import json
import time

print("=" * 60)
print("🧪 Testing Phase 2 Application Server")
print("=" * 60)

urls = {
    'Health Check': 'http://localhost:8000/health',
    'API Docs': 'http://localhost:8000/docs',
    'Home Page': 'http://localhost:8000',
}

for name, url in urls.items():
    print(f"\n📍 Testing {name}: {url}")
    try:
        response = urllib.request.urlopen(url, timeout=5)
        data = response.read().decode()
        print(f"✅ SUCCESS - Status: {response.status}")
        if 'health' in url:
            try:
                health_data = json.loads(data)
                print(f"   Response: {json.dumps(health_data, indent=2)}")
            except:
                print(f"   Response: {data[:100]}...")
    except Exception as e:
        print(f"⏳ Server starting... ({str(e)[:50]})")

print("\n" + "=" * 60)
print("💡 Tip: Open http://localhost:8000/docs in browser")
print("=" * 60)
