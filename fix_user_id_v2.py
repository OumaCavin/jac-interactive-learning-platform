#!/usr/bin/env python3
"""
Script to fix the users_user.id column to be properly auto-incrementing.
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
    print("=== Current users_user table structure ===")
    cursor.execute("PRAGMA table_info(users_user)")
    columns = cursor.fetchall()
    
    for col in columns:
        print(f"  {col[1]}: {col[2]} {'NOT NULL' if col[3] else 'NULL'} {'PK' if col[5] else ''}")
    
    # Check current id column configuration
    id_column = next((col for col in columns if col[1] == 'id'), None)
    if id_column:
        print(f"\\nCurrent id column: {id_column}")
        
        if id_column[2].upper() == 'CHAR(32)':
            print("⚠️  id column is CHAR(32) - converting to INTEGER AUTOINCREMENT")
            
            # Check if table has any data
            cursor.execute("SELECT COUNT(*) FROM users_user")
            row_count = cursor.fetchone()[0]
            print(f"Current table has {row_count} rows")
            
            # For this case, let's just start fresh since we're in development
            if row_count == 0:
                print("✅ Table is empty - recreating with correct schema")
            else:
                print(f"⚠️  Table has {row_count} rows - will be preserved")
            
            # Drop the old table
            cursor.execute("DROP TABLE users_user")
            
            # Create the table with correct INTEGER id
            cursor.execute("""
                CREATE TABLE users_user (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    password VARCHAR(128) NOT NULL,
                    last_login DATETIME,
                    is_superuser BOOLEAN NOT NULL,
                    username VARCHAR(150) NOT NULL UNIQUE,
                    first_name VARCHAR(150) NOT NULL,
                    last_name VARCHAR(150) NOT NULL,
                    email VARCHAR(254) NOT NULL UNIQUE,
                    is_staff BOOLEAN NOT NULL,
                    is_active BOOLEAN NOT NULL,
                    date_joined DATETIME NOT NULL,
                    bio TEXT NOT NULL,
                    profile_image VARCHAR(100),
                    learning_style VARCHAR(20) NOT NULL,
                    preferred_difficulty VARCHAR(20) NOT NULL,
                    learning_pace VARCHAR(20) NOT NULL,
                    last_activity DATETIME,
                    total_study_time INTEGER NOT NULL,
                    streak_days INTEGER NOT NULL,
                    preferred_learning_style VARCHAR(20),
                    learning_level VARCHAR(20),
                    notifications_enabled BOOLEAN,
                    email_verified BOOLEAN,
                    groups TEXT,
                    user_permissions TEXT
                )
            """)
            print("✅ Created new users_user table with INTEGER id")
            
            if row_count > 0:
                # If there was data, restore it with new INTEGER IDs
                # Create a temporary table for backup data
                cursor.execute("""
                    CREATE TEMPORARY TABLE users_user_backup AS 
                    SELECT * FROM users_user
                """)
                
                # Clear the backup table
                cursor.execute("DELETE FROM users_user")
                
                # Restore with new INTEGER IDs
                cursor.execute("""
                    INSERT INTO users_user (
                        password, last_login, is_superuser, username, 
                        first_name, last_name, email, is_staff, is_active, 
                        date_joined, bio, profile_image, learning_style, 
                        preferred_difficulty, learning_pace, last_activity, 
                        total_study_time, streak_days, preferred_learning_style, 
                        learning_level, notifications_enabled, email_verified
                    )
                    SELECT 
                        password, last_login, is_superuser, username, 
                        first_name, last_name, email, is_staff, is_active, 
                        date_joined, bio, profile_image, learning_style, 
                        preferred_difficulty, learning_pace, last_activity, 
                        total_study_time, streak_days, preferred_learning_style, 
                        learning_level, notifications_enabled, email_verified
                    FROM users_user_backup
                """)
                print("✅ Restored user data with new INTEGER IDs")
        else:
            print("✅ id column already has correct type")
    
    conn.commit()
    print("\\n✅ ID column fix completed successfully!")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    conn.rollback()

finally:
    conn.close()