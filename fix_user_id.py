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
            
            # Create a temporary table with the correct structure
            cursor.execute("""
                CREATE TEMPORARY TABLE users_user_backup AS 
                SELECT * FROM users_user
            """)
            print("✅ Backed up existing data")
            
            # Drop the old table
            cursor.execute("DROP TABLE users_user")
            
            # Create the table with correct INTEGER id
            cursor.execute("""
                CREATE TABLE users_user (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    password VARCHAR(128),
                    last_login DATETIME,
                    is_superuser BOOLEAN,
                    username VARCHAR(150) UNIQUE,
                    first_name VARCHAR(150),
                    last_name VARCHAR(150),
                    email VARCHAR(254) UNIQUE,
                    is_staff BOOLEAN,
                    is_active BOOLEAN,
                    date_joined DATETIME,
                    bio TEXT,
                    profile_image VARCHAR(100),
                    learning_style VARCHAR(20),
                    preferred_difficulty VARCHAR(20),
                    learning_pace VARCHAR(20),
                    last_activity DATETIME,
                    total_study_time INTEGER,
                    streak_days INTEGER,
                    preferred_learning_style VARCHAR(20),
                    learning_level VARCHAR(20),
                    notifications_enabled BOOLEAN,
                    email_verified BOOLEAN,
                    groups TEXT,
                    user_permissions TEXT,
                    FOREIGN KEY (groups) REFERENCES auth_group(id),
                    FOREIGN KEY (user_permissions) REFERENCES auth_permission(id)
                )
            """)
            print("✅ Created new users_user table with INTEGER id")
            
            # Restore data (without the old groups and user_permissions that we'll handle separately)
            # For now, just insert the basic user data
            backup_columns = [col[1] for col in cursor.execute("PRAGMA table_info(users_user_backup)").fetchall()]
            print(f"Backup table columns: {backup_columns}")
            
            # Get data from backup
            cursor.execute("SELECT * FROM users_user_backup")
            backup_data = cursor.fetchall()
            
            # Map old CHAR(32) ids to new INTEGER ids
            new_data = []
            for i, row in enumerate(backup_data, 1):
                # Convert CHAR(32) id to INTEGER (just use row index + 1)
                new_row = (i,) + row[1:]  # Replace old id with new INTEGER id
                new_data.append(new_row)
            
            # Insert the data
            placeholders = ','.join(['?' for _ in range(len(new_data[0]))])
            cursor.executemany(f"INSERT INTO users_user VALUES ({placeholders})", new_data)
            print(f"✅ Restored {len(new_data)} user records")
            
            # Update foreign key references in auth tables
            print("🔄 Updating auth tables...")
            
            # Update groups reference
            cursor.execute("UPDATE auth_group SET user_set = REPLACE(user_set, ?, ?)")
            
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