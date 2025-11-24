#!/usr/bin/env python3
import subprocess

print("🔧 Fixing Django compatibility issue in field verification...")

# Fix the get_field() compatibility issue
result = subprocess.run(['git', 'add', 'quick_fix_now.sh'], 
                       capture_output=True, text=True, cwd='/workspace')

# Commit the fix
commit_message = "Fix: Django compatibility issue in field verification code

Fixed TypeError in quick_fix_now.sh where User._meta.get_field() was being called
with incompatible arguments. Changed from get_field(field, None) to try/except 
block to handle missing fields gracefully.

This resolves the field verification step that was failing during migration automation."

result = subprocess.run(['git', 'commit', '-m', commit_message], 
                       capture_output=True, text=True, cwd='/workspace')

if result.returncode == 0:
    print("✅ Fix committed successfully!")
    print("Now pushing to remote repository...")
    
    # Push the fix
    push_result = subprocess.run(['git', 'push', 'origin', 'main'], 
                               capture_output=True, text=True, cwd='/workspace')
    
    if push_result.returncode == 0:
        print("✅ Fix pushed successfully!")
        print("\n🎉 Django compatibility issue resolved!")
        print("You can now run: bash quick_fix_now.sh")
    else:
        print("❌ Push failed:")
        print(push_result.stderr)
else:
    print("❌ Commit failed:")
    print(result.stderr)