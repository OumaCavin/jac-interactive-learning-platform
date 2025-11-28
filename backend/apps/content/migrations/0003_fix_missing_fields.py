# JAC Interactive Learning Platform - Core backend implementation by Cavin Otieno

# Migration to add Content missing fields (COMMENTED OUT - models don't exist)
# This migration is commented out because the referenced models don't exist in models.py

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('content', '0002_initial'),
    ]

    operations = [
        # NOTE: The following operations are commented out because the corresponding models
        # don't exist in the current models.py. These additions were intended for models
        # that were planned but never implemented.
        
        # Add ContentBlock fields (COMMENTED OUT - ContentBlock model doesn't exist)
        # migrations.AddField(
        #     model_name='contentblock',
        #     name='block_type',
        #     field=models.CharField(choices=[('text', 'Text'), ('image', 'Image'), ('video', 'Video'), ('code', 'Code'), ('quiz', 'Quiz')], default='text', max_length=20),
        # ),
        # 
        # migrations.AddField(
        #     model_name='contentblock',
        #     name='order_index',
        #     field=models.IntegerField(default=0, help_text='Order of this block within its content'),
        # ),
        
        # Add LearningModule fields (COMMENTED OUT - LearningModule model doesn't exist)
        # migrations.AddField(
        #     model_name='learningmodule',
        #     name='estimated_duration',
        #     field=models.PositiveIntegerField(default=30, help_text='Estimated duration in minutes'),
        # ),
        # 
        # migrations.AddField(
        #     model_name='learningmodule',
        #     name='prerequisites',
        #     field=models.JSONField(default=list, help_text='Prerequisites for this module'),
        # ),
        
        # Add ContentResource fields (COMMENTED OUT - ContentResource model doesn't exist)
        # migrations.AddField(
        #     model_name='contentresource',
        #     name='resource_type',
        #     field=models.CharField(choices=[('pdf', 'PDF'), ('video', 'Video'), ('link', 'External Link'), ('image', 'Image')], default='pdf', max_length=20),
        # ),
        # 
        # migrations.AddField(
        #     model_name='contentresource',
        #     name='file_size',
        #     field=models.PositiveIntegerField(help_text='File size in bytes'),
        # ),
        
        # Add performance indexes for existing Content model
        # (Uncomment these when corresponding models are implemented)
        
        # migrations.AddIndex(
        #     model_name='content',
        #     index=models.Index(fields=['content_type', 'is_published'], name='content_content_type_published_idx'),
        # ),
        # 
        # migrations.AddIndex(
        #     model_name='content',
        #     index=models.Index(fields=['created_by', 'created_at'], name='content_created_by_created_idx'),
        # ),
    ]