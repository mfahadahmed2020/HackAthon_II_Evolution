import sys
sys.path.insert(0, 'E:\\Python Codes\\HackAthon 2\\Phase II')

from app.config import settings

print("Database URL:", settings.DATABASE_URL[:50] + "...")
print("CORS Origins:", settings.allowed_origins_list)
print("Secret Key:", settings.SECRET_KEY[:10] + "...")
