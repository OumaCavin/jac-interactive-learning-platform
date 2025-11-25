#!/usr/bin/env python
"""
Direct database fix for migration issues
"""
import os
import sys
import django
import sqlite3
from django.conf import settings

def fix_database_directly():
    """Fix the database directly to resolve migration conflicts"""
    
    # Use minimal Django setup to avoid migration issues
    sys.path.insert(0, '/workspace/backend')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings_minimal')
    
    try:
        # Minimal Django setup
        django.setup()
        
        # Connect to database
        db_path = settings.DATABASES['default']['NAME']
        print(f"Using database: {db_path}")
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check current schema for assessmentquestion table
        cursor.execute("PRAGMA table_info(assessment_app_assessmentquestion)")
        columns = cursor.fetchall()
        print("Current assessmentquestion table schema:")
        for col in columns:
            print(f"  {col}")
        
        # Check if assessment column is nullable
        for col in columns:
            if col[1] == 'assessment_id':  # column name in database
                print(f"Assessment column nullable: {not col[3]}")  # col[3] is 'not null'
                break
        
        # Fix the schema by making assessment nullable
        try:
            # First, handle any existing data by setting null values
            cursor.execute("UPDATE assessment_app_assessmentquestion SET assessment_id = NULL WHERE assessment_id IS NOT NULL AND assessment_id = ''")
            
            # Make the column nullable
            cursor.execute("""
                ALTER TABLE assessment_app_assessmentquestion 
                ALTER COLUMN assessment_id INTEGER NULL
            """)
            print("Successfully made assessment_id nullable")
            
        except sqlite3.Error as e:
            print(f"Schema alteration failed: {e}")
            print("Attempting alternative approach...")
            
            # Alternative: create a new table with correct schema
            cursor.execute("""
                CREATE TABLE assessment_app_assessmentquestion_new (
                    question_id TEXT PRIMARY KEY,
                    assessment_id INTEGER NULL,
                    module_id INTEGER NOT NULL,
                    title TEXT NOT NULL,
                    question_text TEXT NOT NULL,
                    question_type TEXT NOT NULL DEFAULT 'multiple_choice',
                    options TEXT DEFAULT '[]',
                    correct_answer TEXT NOT NULL,
                    explanation TEXT DEFAULT '',
                    points REAL NOT NULL DEFAULT 1.0,
                    difficulty_level TEXT NOT NULL DEFAULT 'medium',
                    order INTEGER NOT NULL DEFAULT 0,
                    tags TEXT DEFAULT '[]',
                    learning_objectives TEXT DEFAULT '[]',
                    is_active BOOLEAN NOT NULL DEFAULT 1,
                    version INTEGER NOT NULL DEFAULT 1,
                    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (assessment_id) REFERENCES assessment_app_assessments(id) ON DELETE CASCADE,
                    FOREIGN KEY (module_id) REFERENCES learning_app_modules(id) ON DELETE CASCADE
                )
            """)
            
            # Copy data from old table
            cursor.execute("""
                INSERT INTO assessment_app_assessmentquestion_new 
                SELECT *, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
                FROM assessment_app_assessmentquestion
            """)
            
            # Drop old table and rename new one
            cursor.execute("DROP TABLE assessment_app_assessmentquestion")
            cursor.execute("ALTER TABLE assessment_app_assessmentquestion_new RENAME TO assessment_app_assessmentquestion")
            print("Successfully recreated table with nullable assessment_id")
        
        conn.commit()
        conn.close()
        
        print("Database fix completed!")
        return True
        
    except Exception as e:
        print(f"Database fix failed: {e}")
        return False

if __name__ == "__main__":
    success = fix_database_directly()
    sys.exit(0 if success else 1)