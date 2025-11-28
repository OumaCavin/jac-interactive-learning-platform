#!/usr/bin/env python3
"""
Safe Django Migration Creator
Handles permission issues when creating migrations in Docker containers
"""

import os
import sys
import subprocess
import django
from pathlib import Path

def fix_migration_permissions():
    """Fix permissions for migration directories"""
    migration_dirs = [
        'backend/apps/collaboration/migrations',
        'backend/apps/gamification/migrations',
        'backend/apps/learning/migrations',
        'backend/apps/users/migrations',
        'backend/apps/assessments/migrations',
        'backend/apps/agents/migrations',
        'backend/apps/content/migrations',
        'backend/apps/jac_execution/migrations',
        'backend/apps/knowledge_graph/migrations',
        'backend/apps/search/migrations',
        'backend/apps/progress/migrations'
    ]
    
    print("🔧 Fixing permissions for migration directories...")
    
    for migration_dir in migration_dirs:
        dir_path = Path(migration_dir)
        if dir_path.exists():
            try:
                # Set directory permissions
                os.chmod(dir_path, 0o755)
                
                # Set file permissions within directory
                for file_path in dir_path.glob('*.py'):
                    if file_path.name != '__init__.py':
                        os.chmod(file_path, 0o644)
                        
                print(f"✅ Fixed permissions: {migration_dir}")
            except PermissionError:
                print(f"⚠️  Permission error for: {migration_dir}")
            except Exception as e:
                print(f"❌ Error with {migration_dir}: {e}")
        else:
            print(f"📁 Directory not found: {migration_dir}")

def run_migration_command():
    """Run Django migration command with error handling"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    
    try:
        django.setup()
        
        # Fix permissions first
        fix_migration_permissions()
        
        # Try to create migrations
        print("\n🔄 Creating migrations...")
        
        # Import Django management
        from django.core.management import execute_from_command_line
        
        # Create migrations for collaboration app
        print("→ Creating migrations for collaboration app...")
        execute_from_command_line(['manage.py', 'makemigrations', 'collaboration', '--noinput'])
        
        print("\n✅ Migrations created successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Migration creation failed: {e}")
        return False

if __name__ == '__main__':
    success = run_migration_command()
    sys.exit(0 if success else 1)