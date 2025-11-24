# Generated migration for jac_execution app

from django.db import migrations, models
import uuid
import django.utils.timezone
from django.conf import settings
from django.contrib.auth.models import User


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CodeExecution',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('language', models.CharField(choices=[('jac', 'JAC'), ('python', 'Python')], default='python', max_length=10)),
                ('code', models.TextField()),
                ('stdin', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('running', 'Running'), ('completed', 'Completed'), ('failed', 'Failed'), ('timeout', 'Timeout'), ('error', 'Error')], default='pending', max_length=20)),
                ('stdout', models.TextField(blank=True, null=True)),
                ('stderr', models.TextField(blank=True, null=True)),
                ('output', models.TextField(blank=True, null=True)),
                ('return_code', models.IntegerField(blank=True, null=True)),
                ('execution_time', models.FloatField(blank=True, null=True)),
                ('memory_usage', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('max_execution_time', models.FloatField(default=5.0)),
                ('max_memory', models.IntegerField(default=64)),
                ('max_output_size', models.IntegerField(default=10240)),
                ('user', models.ForeignKey(on_delete=models.CASCADE, related_name='code_executions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Code Execution',
                'verbose_name_plural': 'Code Executions',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='ExecutionTemplate',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('language', models.CharField(choices=[('jac', 'JAC'), ('python', 'Python')], max_length=10)),
                ('code', models.TextField()),
                ('stdin', models.TextField(blank=True, null=True)),
                ('is_public', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.CharField(blank=True, max_length=100)),
                ('tags', models.JSONField(blank=True, default=list)),
                ('created_by', models.ForeignKey(on_delete=models.CASCADE, related_name='execution_templates', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Execution Template',
                'verbose_name_plural': 'Execution Templates',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='CodeExecutionSession',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('session_id', models.CharField(max_length=255, unique=True)),
                ('total_executions', models.IntegerField(default=0)),
                ('successful_executions', models.IntegerField(default=0)),
                ('failed_executions', models.IntegerField(default=0)),
                ('total_execution_time', models.FloatField(default=0.0)),
                ('started_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_activity', models.DateTimeField(auto_now=True)),
                ('ended_at', models.DateTimeField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=models.CASCADE, related_name='execution_sessions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Execution Session',
                'verbose_name_plural': 'Execution Sessions',
                'ordering': ['-started_at'],
            },
        ),
        migrations.CreateModel(
            name='SecuritySettings',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('max_execution_time', models.FloatField(default=5.0)),
                ('max_memory', models.IntegerField(default=64)),
                ('max_output_size', models.IntegerField(default=10240)),
                ('max_code_size', models.IntegerField(default=102400)),
                ('allowed_languages', models.JSONField(default=list)),
                ('enable_sandboxing', models.BooleanField(default=True)),
                ('enable_network_access', models.BooleanField(default=False)),
                ('max_executions_per_minute', models.IntegerField(default=60)),
                ('max_executions_per_hour', models.IntegerField(default=1000)),
                ('blocked_imports', models.JSONField(default=list)),
                ('blocked_functions', models.JSONField(default=list)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Security Settings',
                'verbose_name_plural': 'Security Settings',
            },
        ),
    ]
