#!/usr/bin/env python3
"""
Pre-Migration Hook for Django Migrations
Automatically creates database backup before running migrations
"""

import os
import sys
import django
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from backup_manager import pre_migration_backup

def pre_migration_hook():
    """Django migration pre-hook"""
    print("=" * 60)
    print("🔄 PRE-MIGRATION BACKUP HOOK")
    print("=" * 60)
    
    try:
        success = pre_migration_backup()
        if success:
            print("✅ Pre-migration backup completed successfully")
            print("🚀 Proceeding with migration...")
            return True
        else:
            print("❌ Pre-migration backup failed")
            print("⚠️  Consider running backup manually before proceeding")
            
            # Ask user if they want to continue despite backup failure
            response = input("Continue with migration anyway? (yes/no): ").lower()
            if response == 'yes':
                print("⚠️  Proceeding without backup - data loss possible!")
                return True
            else:
                print("❌ Migration cancelled by user")
                return False
                
    except Exception as e:
        print(f"❌ Pre-migration hook error: {e}")
        return False


# Example usage in Django management commands
# Add this to your manage.py or migration management commands:

"""
# Example integration in manage.py:
import sys
from django.core.management import execute_from_command_line

if len(sys.argv) > 1 and sys.argv[1] == 'migrate':
    from pre_migration_hook import pre_migration_hook
    if not pre_migration_hook():
        sys.exit(1)

execute_from_command_line(sys.argv)
"""

if __name__ == "__main__":
    success = pre_migration_hook()
    sys.exit(0 if success else 1)