#!/usr/bin/env python3
"""
Direct database fix for Django migration interactive prompt issue.
This script bypasses Django to directly fix the migration problem.
"""

import sqlite3
import os
import shutil
from datetime import datetime

def backup_database():
    """Create a backup of the current database"""
    backup_name = f"db_backup_before_fix_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sqlite3"
    shutil.copy2('db.sqlite3', backup_name)
    print(f"Database backed up to: {backup_name}")
    return backup_name

def fix_migration_tables():
    """Fix the Django migration tables directly"""
    
    # Connect to database
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    
    # Check current migration state
    cursor.execute("SELECT name, app FROM django_migrations ORDER BY id")
    migrations = cursor.fetchall()
    print("Current migrations:")
    for migration in migrations:
        print(f"  {migration[1]}: {migration[0]}")
    
    # Remove the problematic migration if it exists
    cursor.execute("""
        DELETE FROM django_migrations 
        WHERE app = 'learning' 
        AND name LIKE '%adaptive_learning%'
    """)
    
    # Reset migration state for learning app
    cursor.execute("""
        DELETE FROM django_migrations 
        WHERE app = 'learning' 
        AND name LIKE '0003_%'
    """)
    
    # Reset all learning app migrations to before the problematic one
    cursor.execute("""
        DELETE FROM django_migrations 
        WHERE app = 'learning' 
        AND name >= '0003_add_adaptive_learning_models'
    """)
    
    # Also clean up schema_migrations table if it exists
    cursor.execute("""
        DELETE FROM django_migrations 
        WHERE app = 'learning' 
        AND name IN ('0003_add_adaptive_learning_models', '0004_fix_spaced_repetition_field')
    """)
    
    conn.commit()
    
    # Check the schema for our table
    cursor.execute("PRAGMA table_info(jac_spaced_repetition_session)")
    columns = cursor.fetchall()
    print("\nCurrent columns in jac_spaced_repetition_session:")
    for col in columns:
        print(f"  {col[1]} ({col[2]})")
    
    # Ensure ease_factor column exists
    cursor.execute("""
        SELECT COUNT(*) FROM pragma_table_info('jac_spaced_repetition_session') 
        WHERE name = 'ease_factor'
    """)
    
    if cursor.fetchone()[0] == 0:
        print("Adding ease_factor column...")
        cursor.execute("""
            ALTER TABLE jac_spaced_repetition_session 
            ADD COLUMN ease_factor FLOAT DEFAULT 2.5
        """)
        
        # Copy data from existing column if it exists
        cursor.execute("""
            UPDATE jac_spaced_repetition_session 
            SET ease_factor = 
                CASE 
                    WHEN easiness_factor IS NOT NULL THEN easiness_factor 
                    ELSE 2.5 
                END
            WHERE ease_factor IS NULL
        """)
    
    conn.commit()
    conn.close()
    print("Database fix completed successfully!")

def reset_django_migrations():
    """Reset Django migration history to avoid conflicts"""
    
    # Create a new migration that properly sets up the models
    migration_content = '''# Fixed migration for adaptive learning features

from django.db import migrations, models
import uuid
from django.conf import settings
from django.db import models as django_models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('learning', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdaptiveChallenge',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('challenge_type', models.CharField(max_length=50)),
                ('difficulty_level', models.CharField(max_length=20)),
                ('content_data', models.JSONField(default=dict)),
                ('solution_data', models.JSONField(default=dict)),
                ('test_cases', models.JSONField(default=list)),
                ('hints', models.JSONField(default=list)),
                ('estimated_time', models.PositiveIntegerField(help_text='Estimated time in minutes')),
                ('success_rate', models.FloatField(default=0.0)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django_models.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'jac_adaptive_challenge',
            },
        ),
        migrations.CreateModel(
            name='SpacedRepetitionSession',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('scheduled_for', models.DateTimeField()),
                ('status', models.CharField(choices=[('scheduled', 'Scheduled'), ('ready', 'Ready'), ('completed', 'Completed'), ('skipped', 'Skipped')], default='scheduled', max_length=20)),
                ('quality_rating', models.PositiveIntegerField(blank=True, null=True)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('next_review', models.DateTimeField(blank=True, null=True)),
                ('review_count', models.PositiveIntegerField(default=0)),
                ('ease_factor', models.FloatField(default=2.5)),
                ('interval_days', models.PositiveIntegerField(default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('challenge', models.ForeignKey(on_delete=django_models.CASCADE, to='learning.adaptivechallenge')),
                ('user', models.ForeignKey(on_delete=django_models.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'jac_spaced_repetition_session',
            },
        ),
        migrations.CreateModel(
            name='UserChallengeAttempt',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('not_started', 'Not Started'), ('in_progress', 'In Progress'), ('completed', 'Completed'), ('failed', 'Failed')], default='not_started', max_length=20)),
                ('score', models.FloatField(blank=True, null=True)),
                ('max_score', models.FloatField(default=100.0)),
                ('attempts_count', models.PositiveIntegerField(default=0)),
                ('time_spent', models.DurationField(default=django_models.DurationField().default)),
                ('responses', models.JSONField(default=dict)),
                ('feedback', models.TextField(blank=True)),
                ('started_at', models.DateTimeField(auto_now_add=True)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('challenge', models.ForeignKey(on_delete=django_models.CASCADE, to='learning.adaptivechallenge')),
                ('user', models.ForeignKey(on_delete=django_models.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'jac_user_challenge_attempt',
            },
        ),
        migrations.CreateModel(
            name='UserDifficultyProfile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('current_difficulty', models.CharField(choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')], default='beginner', max_length=20)),
                ('jac_knowledge_level', models.PositiveIntegerField(default=1)),
                ('problem_solving_level', models.PositiveIntegerField(default=1)),
                ('coding_skill_level', models.PositiveIntegerField(default=1)),
                ('recent_accuracy', models.FloatField(default=0.0)),
                ('success_streak', models.PositiveIntegerField(default=0)),
                ('total_attempts', models.PositiveIntegerField(default=0)),
                ('average_score', models.FloatField(default=0.0)),
                ('preferred_challenge_types', models.JSONField(default=list)),
                ('learning_pace', models.CharField(choices=[('slow', 'Slow'), ('moderate', 'Moderate'), ('fast', 'Fast')], default='moderate', max_length=20)),
                ('last_assessment', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django_models.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'jac_user_difficulty_profile',
            },
        ),
    ]
'''
    
    with open('apps/learning/migrations/0003_adaptive_learning_fixed.py', 'w') as f:
        f.write(migration_content)
    
    # Remove the problematic migration files
    problematic_files = [
        'apps/learning/migrations/0003_add_adaptive_learning_models.py',
        'apps/learning/migrations/0004_fix_spaced_repetition_field.py'
    ]
    
    for file_path in problematic_files:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Removed problematic migration: {file_path}")

if __name__ == "__main__":
    os.chdir('/workspace/backend')
    
    print("=== Django Migration Fix Script ===")
    
    # Backup database first
    backup_file = backup_database()
    
    # Fix migration tables
    fix_migration_tables()
    
    # Reset migration files
    reset_django_migrations()
    
    print(f"\n=== Fix Complete ===")
    print(f"Database backed up to: {backup_file}")
    print("Migration files reset.")
    print("You can now run: python manage.py migrate")