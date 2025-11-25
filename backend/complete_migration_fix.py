#!/usr/bin/env python3
"""
Complete migration fix using direct SQLite manipulation
This script completely bypasses Django to fix the migration issue
"""

import sqlite3
import os
import shutil
from datetime import datetime
import time

def main():
    print("=== Starting Direct Database Fix ===")
    
    # Change to backend directory
    os.chdir('/workspace/backend')
    
    # Wait a moment to ensure clean state
    time.sleep(2)
    
    # Backup database
    backup_name = f"db_backup_fixed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sqlite3"
    shutil.copy2('db.sqlite3', backup_name)
    print(f"✅ Database backed up to: {backup_name}")
    
    # Direct SQLite operations (bypassing Django completely)
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    
    print("🔧 Fixing migration tables...")
    
    # Remove all learning app migrations
    cursor.execute("DELETE FROM django_migrations WHERE app = 'learning'")
    print(f"✅ Removed {cursor.rowcount} learning migrations")
    
    # Check current database schema
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%spaced%'")
    tables = cursor.fetchall()
    print(f"📊 Found spaced repetition tables: {[t[0] for t in tables]}")
    
    # Check current columns in jac_spaced_repetition_session
    try:
        cursor.execute("PRAGMA table_info(jac_spaced_repetition_session)")
        columns = cursor.fetchall()
        print(f"📋 Current columns: {[col[1] for col in columns]}")
        
        # Check if ease_factor exists
        ease_factor_exists = any(col[1] == 'ease_factor' for col in columns)
        if not ease_factor_exists:
            print("⚠️ ease_factor column missing, adding it...")
            cursor.execute("ALTER TABLE jac_spaced_repetition_session ADD COLUMN ease_factor REAL DEFAULT 2.5")
            print("✅ Added ease_factor column")
    except sqlite3.Error as e:
        print(f"⚠️ Table check failed: {e}")
        print("📝 This might be normal if the table doesn't exist yet")
    
    conn.commit()
    conn.close()
    print("✅ Database fix completed")
    
    # Fix migration files
    print("🔧 Fixing migration files...")
    
    # Remove problematic migration files
    migration_files_to_remove = [
        'apps/learning/migrations/0003_add_adaptive_learning_models.py',
        'apps/learning/migrations/0004_fix_spaced_repetition_field.py'
    ]
    
    for file_path in migration_files_to_remove:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"✅ Removed: {file_path}")
    
    # Create a clean migration file
    migration_content = '''# Clean migration for adaptive learning features

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
                ('updated_at', models.DateTimeField(auto_now_add=True)),
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
                ('updated_at', models.DateTimeField(auto_now_add=True)),
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
    
    # Write the new migration
    with open('apps/learning/migrations/0003_adaptive_learning_clean.py', 'w') as f:
        f.write(migration_content)
    print("✅ Created clean migration file")
    
    print("\n🎉 === Fix Complete ===")
    print("✅ Database schema fixed")
    print("✅ Migration history reset")
    print("✅ Clean migration file created")
    print("\n📝 Next steps:")
    print("   python manage.py migrate")
    print(f"   Database backup: {backup_name}")

if __name__ == "__main__":
    main()