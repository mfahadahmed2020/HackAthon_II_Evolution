"""Delete models folder to fix circular import"""
import shutil
import os

models_path = r"E:\Python Codes\HackAthon 2\Phase II\backend\app\models"

if os.path.exists(models_path):
    shutil.rmtree(models_path)
    print(f"✓ Deleted: {models_path}")
else:
    print(f"✓ Folder does not exist: {models_path}")

# Verify deletion
if not os.path.exists(models_path):
    print("✓ SUCCESS: models folder deleted permanently")
else:
    print("✗ ERROR: Folder still exists")
