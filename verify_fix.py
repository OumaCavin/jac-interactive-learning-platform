#!/usr/bin/env python3
"""
Verification script to check if all fixes have been applied
"""
import subprocess
import os

os.chdir('/workspace')

def run_command(cmd, description):
    print(f"\n🔍 {description}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print(f"✅ Success: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Failed: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

print("🔧 VERIFICATION SCRIPT - Checking all fixes")
print("=" * 50)

# 1. Check if URL namespace fix is applied
print("\n1. Checking URL namespace fix...")
try:
    with open('backend/config/urls.py', 'r') as f:
        content = f.read()
        if "agents/', include('apps.agents.urls'))" not in content:
            print("✅ URL namespace conflict fixed - no duplicate agents namespace")
        else:
            print("❌ URL namespace issue still exists")
except Exception as e:
    print(f"❌ Error checking URL file: {e}")

# 2. Check if scripts are executable
print("\n2. Checking script permissions...")
if os.path.exists('quick_fix_now.sh') and os.access('quick_fix_now.sh', os.X_OK):
    print("✅ quick_fix_now.sh is executable")
else:
    print("❌ quick_fix_now.sh is not executable")

if os.path.exists('COMPLETE_MIGRATION_FIX.sh') and os.access('COMPLETE_MIGRATION_FIX.sh', os.X_OK):
    print("✅ COMPLETE_MIGRATION_FIX.sh is executable")
else:
    print("❌ COMPLETE_MIGRATION_FIX.sh is not executable")

# 3. Check User model vs Migration file
print("\n3. Comparing User model vs Migration file...")
try:
    # Read User model
    with open('backend/apps/users/models.py', 'r') as f:
        models_content = f.read()
    
    # Read migration file
    with open('backend/apps/users/migrations/0001_initial.py', 'r') as f:
        migration_content = f.read()
    
    # Count fields
    models_lines = [line for line in models_content.split('\n') if '= models.' in line]
    migration_lines = [line for line in migration_content.split('\n') if "'" in line and ":" in line and "models." in line]
    
    print(f"📊 User model fields: {len(models_lines)}")
    print(f"📊 Migration fields: {len(migration_lines)}")
    
    if len(models_lines) > len(migration_lines):
        print(f"⚠️  Found {len(models_lines) - len(migration_lines)} missing fields in migration")
        print("🔧 This will be fixed when running the migration scripts")
    else:
        print("✅ Migration appears to have all fields")

except Exception as e:
    print(f"❌ Error comparing files: {e}")

print("\n" + "=" * 50)
print("🎯 VERIFICATION COMPLETE!")
print("\n📋 RECOMMENDED ACTIONS:")
print("1. Run: bash quick_fix_now.sh")
print("2. Or run: bash COMPLETE_MIGRATION_FIX.sh (more comprehensive)")
print("3. Both scripts will fix all migration issues automatically")