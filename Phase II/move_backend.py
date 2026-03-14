import os
import shutil

# Create backend directory
os.makedirs(r'E:\Python Codes\HackAthon 2\Phase II\backend', exist_ok=True)
print('✓ backend/ directory created')

# Move app/ to backend/app/
src = r'E:\Python Codes\HackAthon 2\Phase II\app'
dst = r'E:\Python Codes\HackAthon 2\Phase II\backend\app'
if os.path.exists(src):
    shutil.move(src, dst)
    print(f'✓ Moved app/ to backend/app/')
else:
    print(f'✗ Source {src} does not exist')

# Move database/ to backend/database/
src = r'E:\Python Codes\HackAthon 2\Phase II\database'
dst = r'E:\Python Codes\HackAthon 2\Phase II\backend\database'
if os.path.exists(src):
    shutil.move(src, dst)
    print(f'✓ Moved database/ to backend/database/')
else:
    print(f'✗ Source {src} does not exist')

# Move requirements.txt to backend/
src = r'E:\Python Codes\HackAthon 2\Phase II\requirements.txt'
dst = r'E:\Python Codes\HackAthon 2\Phase II\backend\requirements.txt'
if os.path.exists(src):
    shutil.move(src, dst)
    print(f'✓ Moved requirements.txt to backend/')
else:
    print(f'✗ Source {src} does not exist')

# Move .env.example to backend/
src = r'E:\Python Codes\HackAthon 2\Phase II\.env.example'
dst = r'E:\Python Codes\HackAthon 2\Phase II\backend\.env.example'
if os.path.exists(src):
    shutil.move(src, dst)
    print(f'✓ Moved .env.example to backend/')
else:
    print(f'✗ Source {src} does not exist')

print('\n✅ Step 1.1 Complete: Backend structure created')
