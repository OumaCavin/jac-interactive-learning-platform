#!/usr/bin/env python3
"""
Script to add missing columns to users_user table to match the comprehensive User model.
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
    print("=== Current users_user table schema ===")
    cursor.execute("PRAGMA table_info(users_user)")
    columns = cursor.fetchall()
    
    existing_columns = {col[1] for col in columns}
    print("Existing columns:")
    for col in columns:
        print(f"  {col[1]} ({col[2]})")
    
    # Define the columns we need for the comprehensive User model
    required_columns = [
        ('bio', 'TEXT DEFAULT ""'),
        ('profile_image', 'VARCHAR(100)'),
        ('preferred_difficulty', 'VARCHAR(20) DEFAULT "beginner"'),
        ('learning_pace', 'VARCHAR(20) DEFAULT "moderate"'),
        ('total_modules_completed', 'INTEGER DEFAULT 0'),
        ('total_time_spent', 'BIGINT DEFAULT 0'),
        ('current_streak', 'INTEGER DEFAULT 0'),
        ('longest_streak', 'INTEGER DEFAULT 0'),
        ('total_points', 'INTEGER DEFAULT 0'),
        ('level', 'INTEGER DEFAULT 1'),
        ('achievements', 'TEXT DEFAULT "[]"'),
        ('badges', 'TEXT DEFAULT "[]"'),
        ('current_goal', 'VARCHAR(200) DEFAULT ""'),
        ('goal_deadline', 'DATETIME'),
        ('agent_interaction_level', 'VARCHAR(20) DEFAULT "moderate"'),
        ('preferred_feedback_style', 'VARCHAR(20) DEFAULT "detailed"'),
        ('dark_mode', 'BOOLEAN DEFAULT 0'),
        ('email_notifications', 'BOOLEAN DEFAULT 1'),
        ('push_notifications', 'BOOLEAN DEFAULT 1'),
        ('is_verified', 'BOOLEAN DEFAULT 0'),
        ('verification_token', 'VARCHAR(100)'),
        ('verification_token_expires_at', 'DATETIME'),
        ('created_at', 'DATETIME DEFAULT CURRENT_TIMESTAMP'),
        ('updated_at', 'DATETIME DEFAULT CURRENT_TIMESTAMP'),
        ('last_login_at', 'DATETIME'),
        ('last_activity_at', 'DATETIME DEFAULT CURRENT_TIMESTAMP'),
    ]
    
    print("\\n=== Adding missing columns ===")
    added_columns = []
    for col_name, col_definition in required_columns:
        if col_name not in existing_columns:
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
        else:
            print(f"✓ Column {col_name} already exists")
    
    # Update the ID column type if needed (should be CHAR(32) for UUID)
    id_column = next((col for col in columns if col[1] == 'id'), None)
    if id_column and id_column[2] == 'INTEGER':
        print("\\n🔄 Converting id column from INTEGER to CHAR(32) for UUID support...")
        try:
            # Convert to CHAR(32) for UUID
            cursor.execute("ALTER TABLE users_user ADD COLUMN id_new CHAR(32) NOT NULL DEFAULT ''")
            # Generate UUIDs for existing rows
            cursor.execute("UPDATE users_user SET id_new = REPLACE(lower(hex(randomblob(16))), 'x', '')")
            cursor.execute("ALTER TABLE users_user DROP COLUMN id")
            cursor.execute("ALTER TABLE users_user RENAME COLUMN id_new TO id")
            print("✅ Converted id column to CHAR(32) for UUID support")
        except sqlite3.OperationalError as e:
            print(f"⚠️  Could not convert id column: {e}")
    
    conn.commit()
    print(f"\\n✅ Successfully added {len(added_columns)} new columns to users_user table!")
    
    # Final verification
    print("\\n=== Final verification ===")
    cursor.execute("PRAGMA table_info(users_user)")
    final_columns = cursor.fetchall()
    print(f"users_user table now has {len(final_columns)} columns")
    
    # Mark the migration as applied in the migration tracking
    print("\\n=== Marking migration as applied ===")
    cursor.execute("INSERT OR REPLACE INTO django_migrations (app, name, applied) VALUES ('users', '0001_initial', datetime('now'))")
    conn.commit()
    print("✅ Migration marked as applied")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    conn.rollback()

finally:
    conn.close()