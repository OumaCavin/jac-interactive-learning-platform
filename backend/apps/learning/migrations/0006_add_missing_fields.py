# JAC Interactive Learning Platform - Core backend implementation by Cavin Otieno

# Migration to add UserChallengeAttempt missing fields and indexes

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('learning', '0005_add_generation_prompt'),
    ]

    operations = [
        # Add missing fields for UserChallengeAttempt
        migrations.AddField(
            model_name='userchallengeattempt',
            name='started_at',
            field=models.DateTimeField(auto_now_add=True, help_text='When the attempt was started'),
        ),
        
        migrations.AddField(
            model_name='userchallengeattempt',
            name='submitted_at',
            field=models.DateTimeField(null=True, blank=True, help_text='When the attempt was submitted'),
        ),
        
        migrations.AddField(
            model_name='userchallengeattempt',
            name='time_spent_minutes',
            field=models.PositiveIntegerField(default=0, help_text='Time spent in minutes'),
        ),
        
        # Add missing fields for LearningModule
        migrations.AddField(
            model_name='learningmodule',
            name='completion_criteria',
            field=models.JSONField(default=dict, help_text='Criteria for module completion'),
        ),
        
        migrations.AddField(
            model_name='learningmodule',
            name='adaptive_difficulty',
            field=models.BooleanField(default=True, help_text='Whether this module uses adaptive difficulty'),
        ),
        
        # Add performance indexes
        migrations.AddIndex(
            model_name='userchallengeattempt',
            index=models.Index(fields=['user', 'status'], name='learning_user_attempt_status_idx'),
        ),
        
        migrations.AddIndex(
            model_name='userchallengeattempt',
            index=models.Index(fields=['challenge', 'user'], name='learning_user_attempt_challenge_user_idx'),
        ),
        
        migrations.AddIndex(
            model_name='adaptivechallenge',
            index=models.Index(fields=['difficulty_level'], name='learning_adaptive_challenge_difficulty_idx'),
        ),
    ]