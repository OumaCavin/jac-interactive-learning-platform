#!/usr/bin/env python3
"""
Script to add missing timestamp columns to users_user table.
"""
import os
import sys
import sqlite3
import django

# Add backend to Python path
sys.path.insert(0, '/workspace/backend')
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

django.setup()

# Connect to the database
db_path = '/workspace/backend/db.sqlite3'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    print("=== Adding timestamp columns with constant defaults ===")
    
    # Add timestamp columns with constant defaults
    timestamp_columns = [
        ('created_at', 'DATETIME'),
        ('updated_at', 'DATETIME'),
        ('last_activity_at', 'DATETIME'),
    ]
    
    added_columns = []
    for col_name, col_definition in timestamp_columns:
        try:
            alter_sql = f"ALTER TABLE users_user ADD COLUMN {col_name} {col_definition};"
            cursor.execute(alter_sql)
            print(f"✅ Added column: {col_name}")
            added_columns.append(col_name)
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print(f"⚠️  Column {col_name} already exists")
            else:
                print(f"❌ Error adding {col_name}: {e}")
    
    conn.commit()
    print(f"\\n✅ Successfully added {len(added_columns)} timestamp columns!")
    
    # Now try creating superuser again
    print("\\n=== Testing superuser creation ===")
    from django.contrib.auth import get_user_model
    
    User = get_user_model()
    
    try:
        # Try to get existing admin user
        admin_user = User.objects.filter(username='admin').first()
        if admin_user:
            print("✅ Admin user already exists!")
        else:
            print("🔄 Creating new admin user...")
            admin_user = User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123'
            )
            print(f"✅ Successfully created admin user: {admin_user.username}")
            
            # Test that the user has all required fields
            print("\\nTesting user fields...")
            print(f"  total_points: {admin_user.total_points}")
            print(f"  level: {admin_user.level}")
            print(f"  achievements: {len(admin_user.achievements)}")
            print(f"  current_streak: {admin_user.current_streak}")
            print("✅ All user fields accessible!")
            
    except Exception as e:
        print(f"❌ Error creating/testing superuser: {e}")
        import traceback
        traceback.print_exc()

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    conn.rollback()

finally:
    conn.close()