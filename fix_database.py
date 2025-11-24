#!/usr/bin/env python
"""
Script to manually apply the users app migration and populate curriculum
"""
import os
import sys
import django

# Add the backend directory to Python path
sys.path.insert(0, '/workspace/backend')

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jac_platform.settings')

# Setup Django
django.setup()

# Now we can use Django models and management commands
from django.core.management import call_command
from django.db import connection

print("Setting up database schema...")

# Manually apply the users migration
try:
    with connection.cursor() as cursor:
        # Create users_user table with correct schema
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users_user (
                id BIGINT AUTO_INCREMENT PRIMARY KEY,
                password VARCHAR(128) NOT NULL,
                last_login DATETIME NULL,
                is_superuser BOOLEAN NOT NULL,
                username VARCHAR(150) NOT NULL,
                is_staff BOOLEAN NOT NULL,
                is_active BOOLEAN NOT NULL,
                date_joined DATETIME NOT NULL,
                first_name VARCHAR(150) NULL,
                last_name VARCHAR(150) NULL,
                email VARCHAR(254) NOT NULL,
                preferred_learning_style VARCHAR(20) NOT NULL DEFAULT 'visual',
                learning_level VARCHAR(20) NOT NULL DEFAULT 'beginner',
                total_study_time BIGINT NOT NULL DEFAULT 0,
                last_activity DATETIME NULL,
                streak_days INT UNSIGNED NOT NULL DEFAULT 0,
                notifications_enabled BOOLEAN NOT NULL DEFAULT 1,
                email_verified BOOLEAN NOT NULL DEFAULT 0,
                UNIQUE KEY username (username),
                UNIQUE KEY email (email)
            );
        """)
        
        # Create users_userprofile table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users_userprofile (
                id BIGINT AUTO_INCREMENT PRIMARY KEY,
                bio LONGTEXT NULL,
                location VARCHAR(100) NULL,
                website VARCHAR(200) NULL,
                learning_goals LONGTEXT NULL,
                current_goals JSON NULL DEFAULT '[]',
                modules_completed INT UNSIGNED NOT NULL DEFAULT 0,
                lessons_completed INT UNSIGNED NOT NULL DEFAULT 0,
                assessments_completed INT UNSIGNED NOT NULL DEFAULT 0,
                badges JSON NULL DEFAULT '[]',
                achievements JSON NULL DEFAULT '[]',
                average_lesson_score DOUBLE NOT NULL DEFAULT 0.0,
                total_points INT UNSIGNED NOT NULL DEFAULT 0,
                created_at DATETIME NOT NULL,
                updated_at DATETIME NOT NULL,
                user_id BIGINT NOT NULL,
                UNIQUE KEY user_id (user_id),
                FOREIGN KEY (user_id) REFERENCES users_user(id) ON DELETE CASCADE
            );
        """)
        
    print("Database tables created successfully!")
    
except Exception as e:
    print(f"Error creating tables: {e}")

# Now try to populate the curriculum
print("Populating JAC curriculum...")
try:
    call_command('populate_jac_curriculum', verbosity=2)
    print("Curriculum populated successfully!")
except Exception as e:
    print(f"Error populating curriculum: {e}")

print("Setup completed!")