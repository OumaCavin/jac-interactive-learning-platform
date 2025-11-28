# JAC Interactive Learning Platform - Core backend implementation by Cavin Otieno

# Migration to fix gamification app missing fields and constraints

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gamification', '0001_initial'),
    ]

    operations = [
        # Add missing Badge fields
        migrations.AddField(
            model_name='badge',
            name='unlock_conditions',
            field=models.JSONField(default=dict, help_text='Specific conditions to unlock this badge'),
        ),
        
        migrations.AddField(
            model_name='badge',
            name='usage_count',
            field=models.PositiveIntegerField(default=0, help_text='How many times this badge has been awarded'),
        ),
        
        # Add missing Achievement fields
        migrations.AddField(
            model_name='achievement',
            name='unlock_order',
            field=models.PositiveIntegerField(default=0, help_text='Order for unlocking achievements'),
        ),
        
        # Add UserAchievement tracking fields
        migrations.AddField(
            model_name='userachievement',
            name='progress_percentage',
            field=models.FloatField(default=0.0, help_text='Current progress percentage (0-100)'),
        ),
        
        migrations.AddField(
            model_name='userachievement',
            name='last_updated',
            field=models.DateTimeField(auto_now=True, help_text='When progress was last updated'),
        ),
        
        # Add UserPoints additional fields
        migrations.AddField(
            model_name='userpoints',
            name='points_from_achievements',
            field=models.PositiveIntegerField(default=0, help_text='Total points earned from achievements'),
        ),
        
        migrations.AddField(
            model_name='userpoints',
            name='points_from_challenges',
            field=models.PositiveIntegerField(default=0, help_text='Total points earned from challenges'),
        ),
        
        # Add indexes for performance
        migrations.AddIndex(
            model_name='userbadge',
            index=models.Index(fields=['user', 'badge'], name='gamification_user_badge_user_badge_idx'),
        ),
        
        migrations.AddIndex(
            model_name='userbadge',
            index=models.Index(fields=['badge', 'earned_at'], name='gamification_user_badge_badge_earned_idx'),
        ),
        
        migrations.AddIndex(
            model_name='userachievement',
            index=models.Index(fields=['user', 'achievement'], name='gamification_user_achievement_user_achievement_idx'),
        ),
        
        migrations.AddIndex(
            model_name='userachievement',
            index=models.Index(fields=['user', 'is_completed'], name='gamification_user_achievement_user_completed_idx'),
        ),
        
        migrations.AddIndex(
            model_name='userpoints',
            index=models.Index(fields=['user'], name='gamification_user_points_user_idx'),
        ),
    ]