import shutil
import os

src = r"E:\Python Codes\HackAthon 2\Phase II\app\api"
dst = r"E:\Python Codes\HackAthon 2\Phase II\backup_old_api\app_api_backup"

# Create backup
os.makedirs(os.path.dirname(dst), exist_ok=True)
shutil.copytree(src, dst, dirs_exist_ok=True)

# Verify
files = os.listdir(dst)
print(f"Backup complete! Files backed up: {files}")
