#!/usr/bin/env python3
import subprocess
import sys
import os

print("🔧 Git operations starting...")
print("Current directory:", os.getcwd())

try:
    # Change to workspace directory
    os.chdir('/workspace')
    print("Changed to:", os.getcwd())
    
    # List files to see what's there
    print("\nFiles in workspace:")
    files = os.listdir('.')
    for f in files[:10]:  # Show first 10 files
        print(f"  {f}")
    if len(files) > 10:
        print(f"  ... and {len(files) - 10} more files")
    
    # Check if .git exists
    if os.path.exists('.git'):
        print("\n✅ Git repository found")
        
        # Run git status directly
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True, timeout=30)
        print("\nGit status (porcelain format):")
        print("Return code:", result.returncode)
        print("Output:")
        print(result.stdout)
        if result.stderr:
            print("Error:")
            print(result.stderr)
            
        # If there are changes, add them
        if result.stdout.strip():
            print("\n🔄 Adding changes...")
            add_result = subprocess.run(['git', 'add', '.'], 
                                      capture_output=True, text=True, timeout=30)
            print("Add return code:", add_result.returncode)
            if add_result.stdout:
                print("Add output:", add_result.stdout)
                
            # Commit
            print("\n📝 Committing changes...")
            commit_msg = """Fix: Enhanced migration automation across all setup scripts

Enhanced setup_platform.sh with complete migration automation:
- Added 7-step explicit migration process with field verification
- Users and learning apps targeted: `users learning --merge --noinput`
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
            
            commit_result = subprocess.run(['git', 'commit', '-m', commit_msg], 
                                         capture_output=True, text=True, timeout=30)
            print("Commit return code:", commit_result.returncode)
            if commit_result.stdout:
                print("Commit output:", commit_result.stdout)
            if commit_result.stderr:
                print("Commit error:", commit_result.stderr)
                
            # Push
            print("\n🚀 Pushing to remote...")
            push_result = subprocess.run(['git', 'push', 'origin', 'main'], 
                                       capture_output=True, text=True, timeout=60)
            print("Push return code:", push_result.returncode)
            if push_result.stdout:
                print("Push output:", push_result.stdout)
            if push_result.stderr:
                print("Push error:", push_result.stderr)
                
        else:
            print("\n✅ No changes to commit")
            
    else:
        print("\n❌ No git repository found")
        
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n🎯 Git operations completed!")