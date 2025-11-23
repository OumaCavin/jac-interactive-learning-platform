#!/usr/bin/env python3
import subprocess
import sys

def run_cmd(cmd, description):
    print(f"\n=== {description} ===")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30, cwd='/workspace')
        print(f"Return code: {result.returncode}")
        if result.stdout:
            print(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            print(f"STDERR:\n{result.stderr}")
        return result.returncode == 0
    except Exception as e:
        print(f"Exception: {e}")
        return False

# Check current status
run_cmd("git status --porcelain", "Current git status")

# Check if there are changes to commit
result = subprocess.run("git status --porcelain", shell=True, capture_output=True, text=True, timeout=30)
if result.stdout.strip():
    print("\n🔄 Changes detected - proceeding with commit...")
    
    # Add changes
    if run_cmd("git add .", "Staging changes"):
        # Commit 
        commit_msg = "Fix: Enhanced migration automation across all setup scripts\n\nEnhanced setup_platform.sh with complete migration automation:\n- Added 7-step explicit migration process with field verification\n- Users and learning apps targeted: users learning --merge --noinput\n- Automatic User model field checking (22 fields total)\n- Dry-run migration checks to detect unmigrated changes\n- Enhanced superuser creation during migration process\n\nOther enhancements:\n- Updated quick_fix_now.sh with explicit app targeting\n- Created COMPLETE_MIGRATION_FIX.sh for comprehensive fixes\n- Fixed duplicate agents URL namespace in backend/config/urls.py\n- Added ENHANCED_SETUP_VERIFICATION.md documentation\n\nAll migration issues resolved: jac_user table creation, missing fields, URL conflicts, and authentication problems will be fixed automatically."
        
        if run_cmd(f'git commit -m "{commit_msg}"', "Committing changes"):
            # Push
            run_cmd("git push origin main", "Pushing to remote")
else:
    print("\n✅ No changes detected - all changes already committed")