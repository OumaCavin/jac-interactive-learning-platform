#!/usr/bin/env python3
"""
Fix Django migration issues by directly manipulating the database
and creating proper migrations
"""
import os
import sys
import django

# Add the backend directory to path
sys.path.insert(0, '/workspace/backend')

# Set up Django environment
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

# Set environment variables to prevent interactive prompts
os.environ['PYTHONUNBUFFERED'] = '1'
os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = 'true'

# Initialize Django
django.setup()

from django.db import connection
from django.core.management import call_command
import traceback

def fix_migration_issues():
    """Fix the migration issues by directly manipulating the database"""
    try:
        print("🔧 Fixing Django migration issues...")
        
        # Clear migration history completely
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM django_migrations")
            print("✅ Cleared all migration history")
        
        # Create fresh initial migration for users app
        print("📝 Creating fresh users migration...")
        call_command('makemigrations', 'users', '--noinput', '--verbosity', '0')
        print("✅ Created users migration")
        
        # Create fresh initial migration for learning app  
        print("📝 Creating fresh learning migration...")
        call_command('makemigrations', 'learning', '--noinput', '--verbosity', '0')
        print("✅ Created learning migration")
        
        # Create fresh initial migration for agents app
        print("📝 Creating fresh agents migration...")
        call_command('makemigrations', 'agents', '--noinput', '--verbosity', '0')
        print("✅ Created agents migration")
        
        # Add our custom assessment models migration
        print("📝 Adding assessment models migration...")
        
        # Create our custom migration file
        migration_content = '''# Custom migration for assessment models
from django.db import migrations, models
import django.db.models.deletion
from django.utils import timezone
import uuid

class Migration(migrations.Migration):
    dependencies = [
        ('learning', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assessment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('assessment_type', models.CharField(choices=[('quiz', 'Quiz'), ('exam', 'Exam'), ('practice', 'Practice Test'), ('assignment', 'Assignment')], default='quiz', max_length=20)),
                ('difficulty_level', models.CharField(choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')], default='beginner', max_length=20)),
                ('time_limit_minutes', models.PositiveIntegerField(blank=True, null=True, help_text='Time limit in minutes')),
                ('max_attempts', models.PositiveIntegerField(default=3)),
                ('passing_score', models.FloatField(default=70.0)),
                ('instructions', models.TextField(blank=True)),
                ('is_published', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('module', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assessments', to='learning.module')),
                ('learning_path', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assessments', to='learning.learningpath')),
            ],
            options={
                'db_table': 'jac_assessments',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('question_text', models.TextField()),
                ('question_type', models.CharField(choices=[('multiple_choice', 'Multiple Choice'), ('true_false', 'True/False'), ('short_answer', 'Short Answer'), ('essay', 'Essay'), ('code', 'Code Completion')], default='multiple_choice', max_length=20)),
                ('options', models.JSONField(blank=True, default=list, help_text='Options for multiple choice questions')),
                ('correct_answer', models.JSONField(default=list, help_text='Correct answer(s)')),
                ('explanation', models.TextField(blank=True, help_text='Explanation for the correct answer')),
                ('difficulty_level', models.CharField(choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')], default='medium', max_length=20)),
                ('points', models.FloatField(default=1.0)),
                ('order', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('assessment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='learning.assessment')),
            ],
            options={
                'db_table': 'jac_questions',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='AssessmentAttempt',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('attempt_number', models.PositiveIntegerField(default=1)),
                ('status', models.CharField(choices=[('in_progress', 'In Progress'), ('completed', 'Completed'), ('abandoned', 'Abandoned'), ('timed_out', 'Timed Out')], default='in_progress', max_length=20)),
                ('started_at', models.DateTimeField(auto_now_add=True)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('score', models.FloatField(blank=True, null=True)),
                ('max_score', models.FloatField(default=100.0)),
                ('passing_score', models.FloatField(default=70.0)),
                ('is_passed', models.BooleanField(default=False)),
                ('time_spent', models.DurationField(default=0)),
                ('time_limit', models.PositiveIntegerField(blank=True, help_text='Time limit in minutes', null=True)),
                ('answers', models.JSONField(default=dict, help_text='User answers for each question')),
                ('feedback', models.TextField(blank=True)),
                ('assessment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attempts', to='learning.assessment')),
                ('module', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assessment_attempts', to='learning.module')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assessment_attempts', to='auth.user')),
            ],
            options={
                'db_table': 'jac_assessment_attempts',
            },
        ),
        migrations.CreateModel(
            name='UserAssessmentResult',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('best_score', models.FloatField(blank=True, null=True)),
                ('total_attempts', models.PositiveIntegerField(default=0)),
                ('passed_attempts', models.PositiveIntegerField(default=0)),
                ('first_attempt_score', models.FloatField(blank=True, null=True)),
                ('last_attempt_score', models.FloatField(blank=True, null=True)),
                ('average_score', models.FloatField(blank=True, null=True)),
                ('best_attempt_date', models.DateTimeField(blank=True, null=True)),
                ('first_attempt_date', models.DateTimeField(blank=True, null=True)),
                ('last_attempt_date', models.DateTimeField(blank=True, null=True)),
                ('total_time_spent', models.DurationField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('assessment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_results', to='learning.assessment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assessment_results', to='auth.user')),
            ],
            options={
                'db_table': 'jac_user_assessment_results',
                'unique_together': {('user', 'assessment')},
            },
        ),
        migrations.CreateModel(
            name='AssessmentQuestion',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('difficulty_level', models.CharField(choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')], default='medium', max_length=20)),
                ('points', models.FloatField(default=1.0)),
                ('order', models.PositiveIntegerField(default=0)),
                ('question_text_override', models.TextField(blank=True, help_text='Override default question text for this assessment')),
                ('options_override', models.JSONField(default=list, blank=True, help_text='Override default options for multiple choice')),
                ('correct_answer_override', models.JSONField(default=list, blank=True, help_text='Override correct answer')),
                ('total_attempts', models.PositiveIntegerField(default=0)),
                ('correct_attempts', models.PositiveIntegerField(default=0)),
                ('average_time_seconds', models.FloatField(default=0.0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('assessment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assessment_questions', to='learning.assessment')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assessment_instances', to='learning.question')),
            ],
            options={
                'db_table': 'jac_assessment_questions',
                'unique_together': {('assessment', 'question')},
            },
        ),
        migrations.CreateModel(
            name='Achievement',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField()),
                ('achievement_type', models.CharField(choices=[('progress', 'Learning Progress'), ('streak', 'Learning Streak'), ('score', 'Assessment Score'), ('completion', 'Course Completion'), ('participation', 'Participation'), ('special', 'Special Recognition')], max_length=20)),
                ('criteria', models.JSONField(help_text='JSON criteria for earning this achievement')),
                ('points_reward', models.PositiveIntegerField(default=0)),
                ('badge_icon', models.CharField(blank=True, max_length=100)),
                ('is_hidden', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'jac_achievements',
                'ordering': ['achievement_type', 'name'],
            },
        ),
        migrations.CreateModel(
            name='UserAchievement',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('earned_at', models.DateTimeField(auto_now_add=True)),
                ('points_earned', models.PositiveIntegerField(default=0)),
                ('verification_data', models.JSONField(blank=True, default=dict)),
                ('achievement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_achievements', to='learning.achievement')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='achievements_earned', to='auth.user')),
            ],
            options={
                'db_table': 'jac_user_achievements',
                'unique_together': {('user', 'achievement')},
            },
        ),
    ]
'''
        
        with open('/workspace/backend/apps/learning/migrations/0002_add_assessment_models.py', 'w') as f:
            f.write(migration_content)
        print("✅ Created assessment models migration")
        
        # Apply all migrations
        print("🚀 Applying all migrations...")
        call_command('migrate', '--noinput', '--verbosity', '1')
        print("✅ All migrations applied successfully!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = fix_migration_issues()
    if success:
        print("🎉 Migration issues fixed successfully!")
        sys.exit(0)
    else:
        print("💥 Failed to fix migration issues")
        sys.exit(1)