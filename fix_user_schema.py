#!/usr/bin/env python3
"""
Script to manually fix the users_user table schema by adding missing columns.
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
    # Get current table schema
    print("=== Current users_user table schema ===")
    cursor.execute("PRAGMA table_info(users_user)")
    columns = cursor.fetchall()
    
    print("Current columns:")
    for col in columns:
        print(f"  {col[1]} ({col[2]})")
    
    # Define the columns we need based on the migration file
    required_columns = [
        ('preferred_learning_style', 'varchar(20) DEFAULT "visual"'),
        ('learning_level', 'varchar(20) DEFAULT "beginner"'),
        ('total_study_time', 'bigint DEFAULT 0'),
        ('last_activity', 'datetime'),
        ('streak_days', 'integer DEFAULT 0'),
        ('notifications_enabled', 'boolean DEFAULT 1'),
        ('email_verified', 'boolean DEFAULT 0'),
    ]
    
    # Get existing column names
    existing_columns = {col[1] for col in columns}
    
    # Add missing columns
    print("\\n=== Adding missing columns ===")
    for col_name, col_definition in required_columns:
        if col_name not in existing_columns:
            try:
                alter_sql = f"ALTER TABLE users_user ADD COLUMN {col_name} {col_definition};"
                cursor.execute(alter_sql)
                print(f"✅ Added column: {col_name}")
            except sqlite3.OperationalError as e:
                if "duplicate column name" in str(e):
                    print(f"⚠️  Column {col_name} already exists")
                else:
                    print(f"❌ Error adding {col_name}: {e}")
        else:
            print(f"✓ Column {col_name} already exists")
    
    # Check for users_userprofile table
    print("\\n=== Checking users_userprofile table ===")
    cursor.execute("PRAGMA table_info(users_userprofile)")
    profile_columns = cursor.fetchall()
    
    if not profile_columns:
        print("❌ users_userprofile table doesn't exist - will need to create it")
        # We might need to create this table separately
    else:
        print(f"✅ users_userprofile table exists with {len(profile_columns)} columns")
    
    # Commit changes
    conn.commit()
    print("\\n✅ Database schema fixes applied successfully!")
    
    # Verify the changes
    print("\\n=== Final verification ===")
    cursor.execute("PRAGMA table_info(users_user)")
    final_columns = cursor.fetchall()
    print("Final columns in users_user:")
    for col in final_columns:
        print(f"  {col[1]} ({col[2]})")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    conn.rollback()

finally:
    conn.close()