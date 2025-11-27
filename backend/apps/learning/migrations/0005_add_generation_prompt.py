# JAC Interactive Learning Platform - Core backend implementation by Cavin Otieno

# Migration to add generation_prompt field to AdaptiveChallenge

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
        
        # Also add difficulty levels to match current model
        migrations.AlterField(
            model_name='adaptivechallenge',
            name='difficulty_level',
            field=models.CharField(
                choices=[
                    ('very_beginner', 'Very Beginner'),
                    ('beginner', 'Beginner'),
                    ('intermediate', 'Intermediate'),
                    ('advanced', 'Advanced'),
                    ('expert', 'Expert'),
                ],
                max_length=20
            ),
        ),
    ]