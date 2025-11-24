#!/usr/bin/env python

# Simple script to add missing columns to users_user table
import os
import sys

# Add backend to path
sys.path.insert(0, '/workspace/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from django.db import connection

print("🔧 Adding missing columns to users_user table...")

with connection.cursor() as cursor:
    # Add the specific missing columns
    try:
        cursor.execute("ALTER TABLE users_user ADD COLUMN IF NOT EXISTS preferred_learning_style VARCHAR(20) DEFAULT 'visual'")
        print("✅ Added preferred_learning_style column")
        
        cursor.execute("ALTER TABLE users_user ADD COLUMN IF NOT EXISTS learning_level VARCHAR(20) DEFAULT 'beginner'")
        print("✅ Added learning_level column")
        
        cursor.execute("ALTER TABLE users_user ADD COLUMN IF NOT EXISTS total_study_time BIGINT DEFAULT 0")
        print("✅ Added total_study_time column")
        
        cursor.execute("ALTER TABLE users_user ADD COLUMN IF NOT EXISTS last_activity DATETIME NULL")
        print("✅ Added last_activity column")
        
        cursor.execute("ALTER TABLE users_user ADD COLUMN IF NOT EXISTS streak_days INT DEFAULT 0")
        print("✅ Added streak_days column")
        
        cursor.execute("ALTER TABLE users_user ADD COLUMN IF NOT EXISTS notifications_enabled BOOLEAN DEFAULT TRUE")
        print("✅ Added notifications_enabled column")
        
        cursor.execute("ALTER TABLE users_user ADD COLUMN IF NOT EXISTS email_verified BOOLEAN DEFAULT FALSE")
        print("✅ Added email_verified column")
        
        print("✅ All missing columns added successfully!")
        
        # Verify the columns now exist
        cursor.execute("DESCRIBE users_user")
        columns = [row[0] for row in cursor.fetchall()]
        print(f"\n📋 Current columns: {columns}")
        
        # Now try to run the curriculum command
        print("\n🎓 Attempting curriculum population...")
        
        import subprocess
        result = subprocess.run([
            '/tmp/.venv/bin/python', 
            '/workspace/backend/manage.py', 
            'populate_jac_curriculum'
        ], cwd='/workspace/backend', capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            print("🎉 SUCCESS! Curriculum populated successfully!")
            print("Output:", result.stdout)
        else:
            print("❌ Curriculum population failed:")
            print("Error:", result.stderr)
            
    except Exception as e:
        print(f"❌ Error adding columns: {e}")

print("\n🏁 Process completed!")