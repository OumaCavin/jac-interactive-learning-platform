# JAC Interactive Learning Platform - Core backend implementation by Cavin Otieno

# Migration to fix content app missing fields and constraints

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('content', '0002_initial'),
    ]

    operations = [
        # Add missing fields for ContentBlock
        migrations.AddField(
            model_name='contentblock',
            name='interactive_elements',
            field=models.JSONField(default=list, help_text='Interactive elements like quizzes, exercises'),
        ),
        
        migrations.AddField(
            model_name='contentblock',
            name='difficulty_adjustment',
            field=models.JSONField(default=dict, help_text='Rules for difficulty adjustment'),
        ),
        
        migrations.AddField(
            model_name='contentblock',
            name='estimated_read_time',
            field=models.PositiveIntegerField(null=True, blank=True, help_text='Estimated reading time in minutes'),
        ),
        
        # Add LearningModule fields
        migrations.AddField(
            model_name='learningmodule',
            name='completion_criteria',
            field=models.JSONField(default=dict, help_text='Criteria for module completion'),
        ),
        
        migrations.AddField(
            model_name='learningmodule',
            name='prerequisite_modules',
            field=models.JSONField(default=list, help_text='IDs of required prerequisite modules'),
        ),
        
        # Add ContentResource fields
        migrations.AddField(
            model_name='contentresource',
            name='download_count',
            field=models.PositiveIntegerField(default=0, help_text='Number of times this resource has been downloaded'),
        ),
        
        migrations.AddField(
            model_name='contentresource',
            name='resource_type',
            field=models.CharField(choices=[('pdf', 'PDF'), ('video', 'Video'), ('audio', 'Audio'), ('interactive', 'Interactive'), ('code', 'Code'), ('image', 'Image'), ('other', 'Other')], default='other', max_length=20),
        ),
        
        # Add indexes for performance
        migrations.AddIndex(
            model_name='contentblock',
            index=models.Index(fields=['content_type', 'module'], name='content_content_block_type_module_idx'),
        ),
        
        migrations.AddIndex(
            model_name='contentblock',
            index=models.Index(fields=['created_by'], name='content_content_block_created_by_idx'),
        ),
        
        migrations.AddIndex(
            model_name='learningmodule',
            index=models.Index(fields=['difficulty_level'], name='content_learning_module_difficulty_level_idx'),
        ),
        
        migrations.AddIndex(
            model_name='learningmodule',
            index=models.Index(fields=['is_published'], name='content_learning_module_is_published_idx'),
        ),
        
        migrations.AddIndex(
            model_name='contentresource',
            index=models.Index(fields=['resource_type'], name='content_content_resource_resource_type_idx'),
        ),
    ]