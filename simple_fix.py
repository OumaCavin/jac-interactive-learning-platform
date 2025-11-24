#!/usr/bin/env python
import os
import sys

# Add backend to path
sys.path.insert(0, '/workspace/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jac_platform.settings')

import django
django.setup()

from django.db import connection

print("🔧 Fixing database schema...")

with connection.cursor() as cursor:
    # Add missing columns
    columns_to_add = [
        "preferred_learning_style VARCHAR(20) DEFAULT 'visual'",
        "learning_level VARCHAR(20) DEFAULT 'beginner'", 
        "total_study_time BIGINT DEFAULT 0",
        "last_activity DATETIME NULL",
        "streak_days INT DEFAULT 0",
        "notifications_enabled BOOLEAN DEFAULT TRUE",
        "email_verified BOOLEAN DEFAULT FALSE"
    ]
    
    for column_def in columns_to_add:
        column_name = column_def.split()[0]
        try:
            cursor.execute(f"ALTER TABLE users_user ADD COLUMN {column_def}")
            print(f"✅ Added {column_name}")
        except Exception as e:
            if "Duplicate column name" in str(e):
                print(f"✅ {column_name} already exists")
            else:
                print(f"❌ Failed to add {column_name}: {e}")

print("✅ Database schema fixed!")
exec(open('/workspace/backend/manage.py').read(), {'__name__': '__main__'})