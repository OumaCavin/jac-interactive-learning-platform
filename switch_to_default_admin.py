#!/usr/bin/env python
"""
Switch to Default Admin Temporarily
This will help us test if the issue is with custom admin or general admin configuration
"""
import sys
import os
import shutil

# Create backup of current urls.py
urls_path = '/workspace/jac-interactive-learning-platform/backend/config/urls.py'
backup_path = '/workspace/jac-interactive-learning-platform/backend/config/urls.py.custom_backup'

def switch_to_default_admin():
    """Switch to default admin to test if issue is custom admin related"""
    print("🔄 Switching to Default Admin Temporarily")
    print("=" * 45)
    
    # Create backup
    try:
        shutil.copy2(urls_path, backup_path)
        print(f"✅ Created backup: {backup_path}")
    except Exception as e:
        print(f"❌ Backup failed: {e}")
        return False
    
    # Read current urls.py
    try:
        with open(urls_path, 'r') as f:
            content = f.read()
        print("✅ Read current urls.py")
    except Exception as e:
        print(f"❌ Failed to read urls.py: {e}")
        return False
    
    # Switch from custom admin to default admin
    new_content = content.replace(
        "path('admin/', custom_admin_site.urls),",
        "path('admin/', admin.site.urls),"
    )
    
    try:
        with open(urls_path, 'w') as f:
            f.write(new_content)
        print("✅ Switched to default admin site")
        print("📝 Changed line 33: custom_admin_site.urls → admin.site.urls")
        return True
    except Exception as e:
        print(f"❌ Failed to write urls.py: {e}")
        return False

def restore_custom_admin():
    """Restore custom admin configuration"""
    print("\n🔄 Restoring Custom Admin Configuration")
    print("=" * 45)
    
    try:
        shutil.copy2(backup_path, urls_path)
        print("✅ Restored custom admin from backup")
        return True
    except Exception as e:
        print(f"❌ Failed to restore: {e}")
        return False

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'restore':
        restore_custom_admin()
    else:
        success = switch_to_default_admin()
        if success:
            print("\n📋 Next steps:")
            print("1. docker-compose restart backend")
            print("2. Test admin: http://localhost:8000/admin/")
            print("3. If admin works, the issue was with custom admin configuration")
            print("4. To restore custom admin: python /app/switch_to_default_admin.py restore")
        else:
            print("\n❌ Failed to switch admin configuration")