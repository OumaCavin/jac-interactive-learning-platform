# JAC Interactive Learning Platform - Core backend implementation by Cavin Otieno

# Migration to fix jac_execution app missing fields and constraints

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('jac_execution', '0002_initial'),
    ]

    operations = [
        # Add missing fields for CodeExecution
        migrations.AddField(
            model_name='codeexecution',
            name='execution_status',
            field=models.CharField(choices=[('pending', 'Pending'), ('running', 'Running'), ('completed', 'Completed'), ('failed', 'Failed'), ('cancelled', 'Cancelled')], default='pending', max_length=20),
        ),
        
        migrations.AddField(
            model_name='codeexecution',
            name='execution_time_ms',
            field=models.PositiveIntegerField(null=True, blank=True, help_text='Execution time in milliseconds'),
        ),
        
        migrations.AddField(
            model_name='codeexecution',
            name='memory_used_mb',
            field=models.PositiveIntegerField(null=True, blank=True, help_text='Memory usage in MB'),
        ),
        
        migrations.AddField(
            model_name='codeexecution',
            name='cpu_cores_used',
            field=models.PositiveIntegerField(default=1, help_text='Number of CPU cores used'),
        ),
        
        # Add TranslationJob fields
        migrations.AddField(
            model_name='translationjob',
            name='translation_engine',
            field=models.CharField(choices=[('google', 'Google Translate'), ('deepL', 'DeepL'), ('local', 'Local Model')], default='google', max_length=20),
        ),
        
        migrations.AddField(
            model_name='translationjob',
            name='confidence_score',
            field=models.FloatField(null=True, blank=True, help_text='Translation confidence score (0-1)'),
        ),
        
        migrations.AddField(
            model_name='translationjob',
            name='target_language',
            field=models.CharField(max_length=10, help_text='Target language code (e.g., en, es, fr)'),
        ),
        
        # Add CodeExecutionHistory fields
        migrations.AddField(
            model_name='codeexecutionhistory',
            name='execution_environment',
            field=models.JSONField(default=dict, help_text='Execution environment details'),
        ),
        
        migrations.AddField(
            model_name='codeexecutionhistory',
            name='input_parameters',
            field=models.JSONField(default=list, help_text='Input parameters used for execution'),
        ),
        
        # Add performance indexes
        migrations.AddIndex(
            model_name='codeexecution',
            index=models.Index(fields=['status', 'created_at'], name='jac_execution_code_execution_status_created_idx'),
        ),
        
        migrations.AddIndex(
            model_name='codeexecution',
            index=models.Index(fields=['user', 'status'], name='jac_execution_code_execution_user_status_idx'),
        ),
        
        migrations.AddIndex(
            model_name='translationjob',
            index=models.Index(fields=['status', 'created_at'], name='jac_execution_translation_job_status_created_idx'),
        ),
        
        migrations.AddIndex(
            model_name='codeexecutionhistory',
            index=models.Index(fields=['user', 'created_at'], name='jac_execution_code_execution_history_user_created_idx'),
        ),
    ]