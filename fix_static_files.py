#!/usr/bin/env python
"""
Fix Static Files Configuration for Docker
Update settings to use Docker-compatible static file paths
"""
import sys
import os

def fix_static_files_config():
    """Fix static files configuration for Docker environment"""
    
    settings_file = '/workspace/jac-interactive-learning-platform/backend/config/settings.py'
    
    print("🔧 Fixing Static Files Configuration")
    print("=" * 40)
    
    # Read current settings
    try:
        with open(settings_file, 'r') as f:
            content = f.read()
        print("✅ Read current settings.py")
    except Exception as e:
        print(f"❌ Failed to read settings.py: {e}")
        return False
    
    # Fix static root to use Docker-compatible path
    new_content = content.replace(
        "STATIC_ROOT = '/var/www/static'",
        "STATIC_ROOT = BASE_DIR / 'staticfiles'  # Docker-compatible path"
    )
    
    # Write updated settings
    try:
        with open(settings_file, 'w') as f:
            f.write(new_content)
        print("✅ Updated static files configuration")
        print("   Changed: STATIC_ROOT = '/var/www/static'")
        print("   To:      STATIC_ROOT = BASE_DIR / 'staticfiles'")
        return True
    except Exception as e:
        print(f"❌ Failed to write settings.py: {e}")
        return False

if __name__ == "__main__":
    success = fix_static_files_config()
    if success:
        print("\n📋 Next steps:")
        print("1. docker-compose restart backend")
        print("2. docker-compose exec backend python manage.py collectstatic --noinput")
        print("3. Test admin: http://localhost:8000/admin/")
    else:
        print("\n❌ Fix failed")