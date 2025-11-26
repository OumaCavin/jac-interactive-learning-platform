# JAC Interactive Learning Platform - Core backend implementation by Cavin Otieno

# Clean migration for adaptive learning features

from django.db import migrations, models
import uuid
from django.conf import settings
from django.db import models as django_models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('learning', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdaptiveChallenge',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('challenge_type', models.CharField(max_length=50)),
                ('difficulty_level', models.CharField(max_length=20)),
                ('content_data', models.JSONField(default=dict)),
                ('solution_data', models.JSONField(default=dict)),
                ('test_cases', models.JSONField(default=list)),
                ('hints', models.JSONField(default=list)),
                ('estimated_time', models.PositiveIntegerField(help_text='Estimated time in minutes')),
                ('success_rate', models.FloatField(default=0.0)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django_models.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'jac_adaptive_challenge',
            },
        ),
        migrations.CreateModel(
            name='SpacedRepetitionSession',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('scheduled_for', models.DateTimeField()),
                ('status', models.CharField(choices=[('scheduled', 'Scheduled'), ('ready', 'Ready'), ('completed', 'Completed'), ('skipped', 'Skipped')], default='scheduled', max_length=20)),
                ('quality_rating', models.PositiveIntegerField(blank=True, null=True)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('next_review', models.DateTimeField(blank=True, null=True)),
                ('review_count', models.PositiveIntegerField(default=0)),
                ('ease_factor', models.FloatField(default=2.5)),
                ('interval_days', models.PositiveIntegerField(default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('challenge', models.ForeignKey(on_delete=django_models.CASCADE, to='learning.adaptivechallenge')),
                ('user', models.ForeignKey(on_delete=django_models.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'jac_spaced_repetition_session',
            },
        ),
        migrations.CreateModel(
            name='UserChallengeAttempt',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('not_started', 'Not Started'), ('in_progress', 'In Progress'), ('completed', 'Completed'), ('failed', 'Failed')], default='not_started', max_length=20)),
                ('score', models.FloatField(blank=True, null=True)),
                ('max_score', models.FloatField(default=100.0)),
                ('attempts_count', models.PositiveIntegerField(default=0)),
                ('time_spent', models.DurationField(default=django_models.DurationField().default)),
                ('responses', models.JSONField(default=dict)),
                ('feedback', models.TextField(blank=True)),
                ('started_at', models.DateTimeField(auto_now_add=True)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('challenge', models.ForeignKey(on_delete=django_models.CASCADE, to='learning.adaptivechallenge')),
                ('user', models.ForeignKey(on_delete=django_models.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'jac_user_challenge_attempt',
            },
        ),
        migrations.CreateModel(
            name='UserDifficultyProfile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('current_difficulty', models.CharField(choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')], default='beginner', max_length=20)),
                ('jac_knowledge_level', models.PositiveIntegerField(default=1)),
                ('problem_solving_level', models.PositiveIntegerField(default=1)),
                ('coding_skill_level', models.PositiveIntegerField(default=1)),
                ('recent_accuracy', models.FloatField(default=0.0)),
                ('success_streak', models.PositiveIntegerField(default=0)),
                ('total_attempts', models.PositiveIntegerField(default=0)),
                ('average_score', models.FloatField(default=0.0)),
                ('preferred_challenge_types', models.JSONField(default=list)),
                ('learning_pace', models.CharField(choices=[('slow', 'Slow'), ('moderate', 'Moderate'), ('fast', 'Fast')], default='moderate', max_length=20)),
                ('last_assessment', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django_models.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'jac_user_difficulty_profile',
            },
        ),
    ]
