#!/usr/bin/env python
"""
Script to fix the Django migration issue with assessment fields
"""
import os
import sys
import django
from django.db import connection
from django.core.management import call_command

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

def fix_assessment_migration():
    """Fix the assessment field migration issue"""
    
    print("Starting migration fix...")
    
    try:
        # First, let's check the current migration state
        print("Checking migration state...")
        
        # Check if there are existing assessment attempts without assessments
        from apps.assessments.models import AssessmentAttempt, Assessment
        
        existing_attempts = AssessmentAttempt.objects.filter(assessment__isnull=True).count()
        print(f"Found {existing_attempts} assessment attempts without assessment")
        
        if existing_attempts > 0:
            # Create a placeholder assessment
            placeholder_assessment, created = Assessment.objects.get_or_create(
                title="System Placeholder Assessment",
                defaults={
                    'description': "Auto-generated placeholder for migration",
                    'assessment_type': 'quiz',
                    'module_id': 1,  # Assuming there's a module with ID 1
                    'is_published': False
                }
            )
            print(f"Created placeholder assessment: {placeholder_assessment.title}")
            
            # Update existing attempts
            updated = AssessmentAttempt.objects.filter(assessment__isnull=True).update(
                assessment=placeholder_assessment
            )
            print(f"Updated {updated} assessment attempts")
        
        # Now try to run migrations with the --noinput flag to avoid prompts
        print("Running migrations...")
        call_command('migrate', interactive=False, verbosity=1)
        
        print("Migration completed successfully!")
        
    except Exception as e:
        print(f"Error during migration: {e}")
        print("Attempting alternative approach...")
        
        try:
            # Alternative approach - manually fix the migration order
            from django.db import migrations
            
            # Create a simple migration that just makes the field nullable
            call_command('makemigrations', 'assessments', verbosity=1)
            
            # Try migrate again
            call_command('migrate', interactive=False, verbosity=1)
            
            print("Alternative migration approach completed!")
            
        except Exception as e2:
            print(f"Alternative approach also failed: {e2}")
            return False
    
    return True

if __name__ == "__main__":
    success = fix_assessment_migration()
    sys.exit(0 if success else 1)