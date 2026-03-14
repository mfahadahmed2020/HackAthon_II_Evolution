import os
import shutil

# Move Python test files to backend/
test_files = [
    'test_app_import.py',
    'test_config.py',
    'test_db.py',
    'test_imports.py',
    'test_imports_simple.py',
    'test_neon_connection.py',
    'test_neon_final.py',
    'test_phase2.py',
    'test_server.py',
    'verify_models.py',
    'verify_phase2_static.py',
    'run_server.py',
    'start_server.py',
    'start_server.bat',
    'debug_import.py',
    'check_python.py',
    'check_deps.py'
]

for file in test_files:
    src = rf'E:\Python Codes\HackAthon 2\Phase II\{file}'
    dst = rf'E:\Python Codes\HackAthon 2\Phase II\backend\{file}'
    if os.path.exists(src):
        shutil.move(src, dst)
        print(f'✓ Moved {file} to backend/')
    else:
        print(f'- Skipped {file} (not found)')

# Create backend/.env file
env_content = """# Application Configuration
APP_NAME=Phase 2 Todo App - Backend
APP_VERSION=2.0.0
DEBUG=True
APP_ENV=development

# Server
HOST=0.0.0.0
PORT=8000

# Database (Neon PostgreSQL)
DATABASE_URL=postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require

# JWT
SECRET_KEY=your-super-secret-jwt-key-here-make-sure-it-is-at-least-32-characters-long
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# API Prefix (Route Fix)
API_PREFIX=/api

# CORS (Next.js frontend ke liye)
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000

# Better Auth
BETTER_AUTH_SECRET=u7WfX5chxDxBIa332yRiZl8KyJ0Fbkxb
BETTER_AUTH_URL=http://localhost:3000

# Frontend URLs
NEXT_PUBLIC_APP_URL=http://localhost:3000
NEXT_PUBLIC_API_URL=http://localhost:8000
"""

with open(r'E:\Python Codes\HackAthon 2\Phase II\backend\.env', 'w') as f:
    f.write(env_content)
print('✓ Created backend/.env file')

print('\n✅ Step 1.1 Complete: All backend files moved and configured')
