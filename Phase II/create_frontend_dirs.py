import os
import json

# Create frontend directory structure
frontend_dirs = [
    'frontend',
    'frontend/app',
    'frontend/app/login',
    'frontend/app/register',
    'frontend/app/dashboard',
    'frontend/app/api/auth/[...nextauth]',
    'frontend/components',
    'frontend/public',
    'frontend/public/images',
    'frontend/public/icons',
    'frontend/lib',
    'frontend/styles'
]

for dir_path in frontend_dirs:
    full_path = rf'E:\Python Codes\HackAthon 2\Phase II\{dir_path}'
    os.makedirs(full_path, exist_ok=True)
    print(f'✓ Created {dir_path}/')

print('\n✅ Frontend directory structure created')
