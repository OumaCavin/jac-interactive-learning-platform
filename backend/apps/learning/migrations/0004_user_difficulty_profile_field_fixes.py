# JAC Interactive Learning Platform - Core backend implementation by Cavin Otieno

# Migration to fix UserDifficultyProfile field conflicts and add missing fields

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('learning', '0003_adaptive_learning_clean'),
    ]

    operations = [
        # Rename the conflicting field
        migrations.RenameField(
            model_name='userdifficultyprofile',
            old_name='last_assessment',
            new_name='last_difficulty_change',
        ),
        
        # Add missing fields that are in the current model but not in database
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
        
        # Update difficulty levels to match current model
        migrations.AlterField(
            model_name='userdifficultyprofile',
            name='current_difficulty',
            field=models.CharField(
                choices=[
                    ('very_beginner', 'Very Beginner'),
                    ('beginner', 'Beginner'),
                    ('intermediate', 'Intermediate'),
                    ('advanced', 'Advanced'),
                    ('expert', 'Expert'),
                ],
                default='beginner',
                max_length=20
            ),
        ),
    ]