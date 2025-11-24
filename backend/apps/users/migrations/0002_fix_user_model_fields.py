# Migration to fix User model field alignment issues
# This resolves conflicts between migration schema and current model definition

from django.db import migrations, models
from django.utils import timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        # Add the missing goal_deadline field that exists in current model
        migrations.AddField(
            model_name='user',
            name='goal_deadline',
            field=models.DateTimeField(blank=True, null=True),
        ),
        
        # Add additional fields that exist in current User model but not in migration
        migrations.AddField(
            model_name='user',
            name='total_modules_completed',
            field=models.PositiveIntegerField(default=0),
        ),
        
        migrations.AddField(
            model_name='user',
            name='total_time_spent',
            field=models.DurationField(default=0),
        ),
        
        migrations.AddField(
            model_name='user',
            name='current_streak',
            field=models.PositiveIntegerField(default=0),
        ),
        
        migrations.AddField(
            model_name='user',
            name='longest_streak',
            field=models.PositiveIntegerField(default=0),
        ),
        
        migrations.AddField(
            model_name='user',
            name='total_points',
            field=models.PositiveIntegerField(default=0),
        ),
        
        migrations.AddField(
            model_name='user',
            name='level',
            field=models.PositiveIntegerField(default=1),
        ),
        
        migrations.AddField(
            model_name='user',
            name='achievements',
            field=models.JSONField(default=list, blank=True),
        ),
        
        migrations.AddField(
            model_name='user',
            name='badges',
            field=models.JSONField(default=list, blank=True),
        ),
        
        migrations.AddField(
            model_name='user',
            name='current_goal',
            field=models.CharField(blank=True, max_length=200),
        ),
        
        migrations.AddField(
            model_name='user',
            name='agent_interaction_level',
            field=models.CharField(choices=[('minimal', 'Minimal Interaction'), ('moderate', 'Moderate Support'), ('high', 'High Support')], default='moderate', max_length=20),
        ),
        
        migrations.AddField(
            model_name='user',
            name='preferred_feedback_style',
            field=models.CharField(choices=[('detailed', 'Detailed Feedback'), ('brief', 'Brief Feedback'), ('encouraging', 'Encouraging Only')], default='detailed', max_length=20),
        ),
        
        migrations.AddField(
            model_name='user',
            name='dark_mode',
            field=models.BooleanField(default=False),
        ),
        
        migrations.AddField(
            model_name='user',
            name='notifications_enabled',
            field=models.BooleanField(default=True),
        ),
        
        migrations.AddField(
            model_name='user',
            name='email_notifications',
            field=models.BooleanField(default=True),
        ),
        
        migrations.AddField(
            model_name='user',
            name='push_notifications',
            field=models.BooleanField(default=True),
        ),
        
        migrations.AddField(
            model_name='user',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
        
        migrations.AddField(
            model_name='user',
            name='verification_token',
            field=models.CharField(max_length=100, null=True, blank=True, unique=True),
        ),
        
        migrations.AddField(
            model_name='user',
            name='verification_token_expires_at',
            field=models.DateTimeField(null=True, blank=True),
        ),
        
        migrations.AddField(
            model_name='user',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        
        migrations.AddField(
            model_name='user',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        
        migrations.AddField(
            model_name='user',
            name='last_login_at',
            field=models.DateTimeField(null=True, blank=True),
        ),
        
        # Update last_activity field to have proper auto_now_add behavior
        migrations.AlterField(
            model_name='user',
            name='last_activity',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]