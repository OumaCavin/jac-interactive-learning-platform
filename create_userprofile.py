#!/usr/bin/env python3
"""
Script to create the users_userprofile table and mark migration as applied.
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
    # Create users_userprofile table based on migration file
    print("=== Creating users_userprofile table ===")
    
    create_profile_sql = """
    CREATE TABLE IF NOT EXISTS users_userprofile (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id CHAR(32) NOT NULL,
        bio TEXT DEFAULT '',
        location VARCHAR(100) DEFAULT '',
        website VARCHAR(200) DEFAULT '',
        learning_goals TEXT DEFAULT '',
        current_goals TEXT DEFAULT '[]',
        modules_completed INTEGER DEFAULT 0,
        lessons_completed INTEGER DEFAULT 0,
        assessments_completed INTEGER DEFAULT 0,
        badges TEXT DEFAULT '[]',
        achievements TEXT DEFAULT '[]',
        average_lesson_score REAL DEFAULT 0.0,
        total_points INTEGER DEFAULT 0,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users_user(id) ON DELETE CASCADE
    );
    """
    
    cursor.execute(create_profile_sql)
    print("✅ Created users_userprofile table")
    
    # Now we need to mark the migration as applied
    # First, let's update the migration record in the database
    
    # Check if migration record exists
    cursor.execute("SELECT name FROM django_migrations WHERE app = 'users' AND name = '0001_initial'")
    migration_exists = cursor.fetchone()
    
    if migration_exists:
        print("Migration record already exists in django_migrations")
    else:
        # Add the migration record
        cursor.execute("""
            INSERT INTO django_migrations (app, name, applied)
            VALUES ('users', '0001_initial', datetime('now'))
        """)
        print("✅ Added migration record to django_migrations")
    
    conn.commit()
    print("\\n✅ users_userprofile table created and migration marked as applied!")
    
    # Verify
    print("\\n=== Verification ===")
    cursor.execute("PRAGMA table_info(users_userprofile)")
    profile_columns = cursor.fetchall()
    print(f"users_userprofile table created with {len(profile_columns)} columns")
    
    cursor.execute("SELECT COUNT(*) FROM django_migrations WHERE app = 'users'")
    user_migrations = cursor.fetchone()[0]
    print(f"Total migrations recorded for users app: {user_migrations}")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    conn.rollback()

finally:
    conn.close()