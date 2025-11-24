#!/usr/bin/env python
"""
Direct database schema fix and curriculum population
"""

import os
import sys

# Set environment variables
os.environ['DJANGO_SETTINGS_MODULE'] = 'jac_platform.settings'
os.environ['PYTHONPATH'] = '/workspace/backend:/tmp/.venv/lib/python3.12/site-packages'

# Add backend to Python path
sys.path.insert(0, '/workspace/backend')

# Import Django
import django
django.setup()

# Import database modules
from django.db import connection
import subprocess

def fix_database_schema():
    """Fix the database schema by adding missing columns"""
    
    print("🔧 Fixing database schema...")
    
    try:
        with connection.cursor() as cursor:
            # Check current schema
            cursor.execute("DESCRIBE users_user")
            columns = [row[0] for row in cursor.fetchall()]
            print(f"Current columns: {columns}")
            
            # Add missing columns
            missing_columns = {
                'preferred_learning_style': 'VARCHAR(20) DEFAULT "visual"',
                'learning_level': 'VARCHAR(20) DEFAULT "beginner"',
                'total_study_time': 'BIGINT DEFAULT 0',
                'last_activity': 'DATETIME NULL',
                'streak_days': 'INT DEFAULT 0',
                'notifications_enabled': 'BOOLEAN DEFAULT TRUE',
                'email_verified': 'BOOLEAN DEFAULT FALSE'
            }
            
            for column_name, column_def in missing_columns.items():
                if column_name not in columns:
                    print(f"➕ Adding column: {column_name}")
                    try:
                        cursor.execute(f"ALTER TABLE users_user ADD COLUMN {column_name} {column_def}")
                        print(f"✅ Added {column_name}")
                    except Exception as e:
                        print(f"⚠️  Could not add {column_name}: {e}")
                else:
                    print(f"✅ {column_name} already exists")
            
        print("✅ Database schema fix completed!")
        return True
        
    except Exception as e:
        print(f"❌ Database fix failed: {e}")
        return False

def run_curriculum_command():
    """Run the curriculum population command"""
    
    print("🎓 Running curriculum population...")
    
    try:
        # Try running the command
        result = subprocess.run([
            '/tmp/.venv/bin/python', 
            '/workspace/backend/manage.py', 
            'populate_jac_curriculum'
        ], 
        cwd='/workspace/backend', 
        capture_output=True, 
        text=True, 
        timeout=180
        )
        
        print(f"Return code: {result.returncode}")
        
        if result.stdout:
            print("📝 Output:")
            print(result.stdout)
        
        if result.stderr:
            print("⚠️  Errors/Warnings:")
            print(result.stderr)
            
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print("⏰ Command timed out")
        return False
    except Exception as e:
        print(f"❌ Command failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting JAC Curriculum Setup...")
    
    # Fix database schema
    if fix_database_schema():
        print("✅ Database schema fixed successfully!")
        
        # Run curriculum population
        if run_curriculum_command():
            print("🎉 Curriculum populated successfully!")
        else:
            print("⚠️  Curriculum population encountered issues")
    else:
        print("❌ Database schema fix failed")
    
    print("\n📊 Setup process completed!")