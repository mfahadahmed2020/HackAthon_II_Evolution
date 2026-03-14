import shutil

# Delete old api directory
shutil.rmtree(r"E:\Python Codes\HackAthon 2\Phase II\app\api")
print("Old app/api/ deleted successfully")

# Verify deletion
import os
if not os.path.exists(r"E:\Python Codes\HackAthon 2\Phase II\app\api"):
    print("✓ Verified: app/api/ no longer exists")
else:
    print("✗ Error: app/api/ still exists")
