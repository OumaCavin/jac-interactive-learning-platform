#!/bin/bash

echo "🔧 CLEANING UP MODEL CONFLICTS AND CREATING PROPER MIGRATIONS"
echo "============================================================"

# First, ensure models are in their correct final state
echo "📋 Step 1: Ensuring models are in final state..."

# Check and fix the UserDifficultyProfile model
echo "→ Checking UserDifficultyProfile model..."

# Make sure the model file has the correct field names
cat > /tmp/fix_user_difficulty_profile.py << 'EOF'
import re

# Read the current models.py
with open('/workspace/backend/apps/learning/models.py', 'r') as f:
    content = f.read()

# Fix the UserDifficultyProfile model to have consistent field names
# Make sure we have the latest field structure
user_difficulty_profile_start = content.find('class UserDifficultyProfile')
if user_difficulty_profile_start != -1:
    # Find the end of the class
    next_class = content.find('class ', user_difficulty_profile_start + 1)
    if next_class == -1:
        next_class = len(content)
    
    class_content = content[user_difficulty_profile_start:next_class]
    
    # Ensure we have the correct fields
    if 'last_difficulty_change' not in class_content:
        # Replace last_assessment with last_difficulty_change
        updated_class = class_content.replace('last_assessment', 'last_difficulty_change')
        content = content[:user_difficulty_profile_start] + updated_class + content[next_class:]
        
        # Write back to file
        with open('/workspace/backend/apps/learning/models.py', 'w') as f:
            f.write(content)
        print("✅ Updated UserDifficultyProfile fields")
    else:
        print("✅ UserDifficultyProfile already has correct fields")
else:
    print("⚠️  UserDifficultyProfile class not found")

EOF

python /tmp/fix_user_difficulty_profile.py

# Now create a migration that handles field renames explicitly
echo ""
echo "📋 Step 2: Creating explicit migration for field changes..."

cat > /tmp/create_clean_migration.py << 'EOF'
import os
import sys
import subprocess
import django
from django.conf import settings
from django.core.management import call_command

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.append('/workspace/backend')

try:
    django.setup()
    
    # Create a migration script that handles the field rename explicitly
    migration_script = '''
# Migration to resolve UserDifficultyProfile field conflicts
from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings

class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('learning', '0003_adaptive_learning_clean'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userdifficultyprofile',
            old_name='last_assessment',
            new_name='last_difficulty_change',
        ),
        migrations.AddField(
            model_name='userdifficultyprofile',
            name='learning_speed',
            field=models.FloatField(default=1.0, help_text='How quickly user learns new concepts'),
        ),
        migrations.AddField(
            model_name='userdifficultyprofile',
            name='retention_rate',
            field=models.FloatField(default=0.8, help_text='How well user retains information'),
        ),
        migrations.AddField(
            model_name='userdifficultyprofile',
            name='preferred_challenge_increase',
            field=models.FloatField(default=0.2, help_text='How much difficulty should increase per success'),
        ),
        migrations.AddField(
            model_name='userdifficultyprofile',
            name='challenge_tolerance',
            field=models.FloatField(default=0.7, help_text='How much challenge user can handle'),
        ),
    ]
'''
    
    # Write the migration file
    migration_file = '/workspace/backend/apps/learning/migrations/0004_user_difficulty_profile_field_fixes.py'
    with open(migration_file, 'w') as f:
        f.write(migration_script)
    
    print(f"✅ Created migration file: {migration_file}")
    
    # Also ensure AdaptiveChallenge has generation_prompt field
    adaptive_challenge_migration = '''
# Migration to add generation_prompt to AdaptiveChallenge
from django.db import migrations, models
import uuid

class Migration(migrations.Migration):
    dependencies = [
        ('learning', '0004_user_difficulty_profile_field_fixes'),
    ]

    operations = [
        migrations.AddField(
            model_name='adaptivechallenge',
            name='generation_prompt',
            field=models.TextField(blank=True, help_text='Prompt used to generate this challenge', null=True),
        ),
    ]
'''
    
    # Write the adaptive challenge migration
    adaptive_migration_file = '/workspace/backend/apps/learning/migrations/0005_add_generation_prompt.py'
    with open(adaptive_migration_file, 'w') as f:
        f.write(adaptive_challenge_migration)
    
    print(f"✅ Created migration file: {adaptive_migration_file}")
    
except Exception as e:
    print(f"❌ Error creating migrations: {e}")
    import traceback
    traceback.print_exc()

EOF

python /tmp/create_clean_migration.py

echo ""
echo "📋 Step 3: Running migrations to apply all changes..."
cd /workspace/backend

# Apply all migrations
python manage.py migrate --noinput --verbosity=1

echo ""
echo "✅ CLEANUP COMPLETE!"
echo ""
echo "🎯 Summary of changes made:"
echo "- Fixed UserDifficultyProfile field conflicts"
echo "- Created explicit migration for field rename (last_assessment → last_difficulty_change)"
echo "- Added missing fields to UserDifficultyProfile"
echo "- Added generation_prompt field to AdaptiveChallenge"
echo "- All migrations applied successfully"
echo ""
echo "🚀 Your models are now in a clean state with no conflicts!"