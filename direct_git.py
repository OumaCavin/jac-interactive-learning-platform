#!/usr/bin/env python3
import subprocess
import os

os.chdir('/workspace')

print("🔧 Executing git operations...")

# Step 1: Add files
print("Step 1: Adding files...")
try:
    result = subprocess.run(['git', 'add', '.'], capture_output=True, text=True, timeout=30)
    print(f"Result: {result.returncode}")
    print(f"Output: {result.stdout}")
    if result.stderr:
        print(f"Error: {result.stderr}")
except Exception as e:
    print(f"Exception: {e}")

print("\nStep 2: Checking status...")
try:
    result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True, timeout=30)
    print(f"Result: {result.returncode}")
    print(f"Output: {result.stdout}")
    if result.stderr:
        print(f"Error: {result.stderr}")
except Exception as e:
    print(f"Exception: {e}")

print("\nStep 3: Committing...")
commit_msg = """Fix: Enhanced migration automation across all setup scripts

Enhanced setup_platform.sh with complete migration automation:
- Added 7-step explicit migration process with field verification
- Users and learning apps targeted: users learning --merge --noinput
- Automatic User model field checking (22 fields total)
- Dry-run migration checks to detect unmigrated changes
- Enhanced superuser creation during migration process

Other enhancements:
- Updated quick_fix_now.sh with explicit app targeting
- Created COMPLETE_MIGRATION_FIX.sh for comprehensive fixes
- Fixed duplicate agents URL namespace in backend/config/urls.py
- Added ENHANCED_SETUP_VERIFICATION.md documentation

All migration issues resolved: jac_user table creation, missing fields,
URL conflicts, and authentication problems will be fixed automatically."""

try:
    result = subprocess.run(['git', 'commit', '-m', commit_msg], capture_output=True, text=True, timeout=30)
    print(f"Result: {result.returncode}")
    print(f"Output: {result.stdout}")
    if result.stderr:
        print(f"Error: {result.stderr}")
except Exception as e:
    print(f"Exception: {e}")

print("\nStep 4: Pushing...")
try:
    result = subprocess.run(['git', 'push', 'origin', 'main'], capture_output=True, text=True, timeout=60)
    print(f"Result: {result.returncode}")
    print(f"Output: {result.stdout}")
    if result.stderr:
        print(f"Error: {result.stderr}")
except Exception as e:
    print(f"Exception: {e}")

print("\n✅ Git operations completed!")