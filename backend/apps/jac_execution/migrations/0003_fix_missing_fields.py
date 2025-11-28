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
        
        # Add additional CodeExecution fields (keeping existing fields intact)
        migrations.AddField(
            model_name='codeexecution',
            name='status_details',
            field=models.TextField(blank=True, null=True, help_text='Additional status details or error messages'),
        ),
        
        migrations.AddField(
            model_name='codeexecution',
            name='user_agent',
            field=models.CharField(max_length=255, blank=True, null=True, help_text='User agent string for execution tracking'),
        ),
        
        # Add performance indexes for CodeExecution
        migrations.AddIndex(
            model_name='codeexecution',
            index=models.Index(fields=['status', 'created_at'], name='jac_execution_code_execution_status_created_idx'),
        ),
        
        migrations.AddIndex(
            model_name='codeexecution',
            index=models.Index(fields=['user', 'status'], name='jac_execution_code_execution_user_status_idx'),
        ),
        
        # Add index for CodeExecutionSession
        migrations.AddIndex(
            model_name='codeexecutionsession',
            index=models.Index(fields=['user', 'is_active'], name='jac_execution_code_execution_session_user_active_idx'),
        ),
    ]