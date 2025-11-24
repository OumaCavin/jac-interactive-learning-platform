# Generated migration for adding missing models

from django.db import migrations, models
import django.db.models.deletion
from django.utils import timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('learning', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssessmentAttempt',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('attempt_number', models.PositiveIntegerField(default=1)),
                ('status', models.CharField(choices=[('in_progress', 'In Progress'), ('completed', 'Completed'), ('abandoned', 'Abandoned'), ('timed_out', 'Timed Out')], default='in_progress', max_length=20)),
                ('started_at', models.DateTimeField(auto_now_add=True)),
                ('completed_at', models.DateTimeField(null=True, blank=True)),
                ('score', models.FloatField(null=True, blank=True)),
                ('max_score', models.FloatField(default=100.0)),
                ('passing_score', models.FloatField(default=70.0)),
                ('is_passed', models.BooleanField(default=False)),
                ('time_spent', models.DurationField(default=0)),
                ('time_limit', models.PositiveIntegerField(blank=True, help_text='Time limit in minutes', null=True)),
                ('answers', models.JSONField(default=dict, help_text='User answers for each question')),
                ('feedback', models.TextField(blank=True)),
                ('assessment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attempts', to='learning.assessment')),
                ('module', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assessment_attempts', to='learning.module')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assessment_attempts', to='auth.user')),
            ],
            options={
                'db_table': 'jac_assessment_attempts',
            },
        ),
        migrations.CreateModel(
            name='AssessmentQuestion',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('difficulty_level', models.CharField(choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')], default='medium', max_length=20)),
                ('points', models.FloatField(default=1.0)),
                ('order', models.PositiveIntegerField(default=0)),
                ('question_text_override', models.TextField(blank=True, help_text='Override default question text for this assessment')),
                ('options_override', models.JSONField(default=list, blank=True, help_text='Override default options for multiple choice')),
                ('correct_answer_override', models.JSONField(default=list, blank=True, help_text='Override correct answer')),
                ('total_attempts', models.PositiveIntegerField(default=0)),
                ('correct_attempts', models.PositiveIntegerField(default=0)),
                ('average_time', models.FloatField(default=0.0, help_text='Average time in seconds')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('assessment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assessment_questions', to='learning.assessment')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assessment_links', to='learning.question')),
            ],
            options={
                'db_table': 'jac_assessment_questions',
            },
        ),
        migrations.CreateModel(
            name='Achievement',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField()),
                ('achievement_type', models.CharField(choices=[('completion', 'Completion'), ('performance', 'Performance'), ('streak', 'Streak'), ('skill', 'Skill'), ('engagement', 'Engagement'), ('collaboration', 'Collaboration')], max_length=20)),
                ('rarity', models.CharField(choices=[('common', 'Common'), ('uncommon', 'Uncommon'), ('rare', 'Rare'), ('epic', 'Epic'), ('legendary', 'Legendary')], default='common', max_length=20)),
                ('requirements', models.JSONField(default=dict, help_text='Requirements to unlock this achievement')),
                ('icon', models.CharField(blank=True, help_text='Icon URL or name', max_length=200)),
                ('badge_color', models.CharField(default='blue', help_text='CSS color class', max_length=20)),
                ('unlock_count', models.PositiveIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'jac_achievements',
            },
        ),
        migrations.CreateModel(
            name='UserAchievement',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('unlocked_at', models.DateTimeField(auto_now_add=True)),
                ('context', models.JSONField(default=dict, help_text='Context when achievement was unlocked')),
                ('progress_at_unlock', models.JSONField(default=dict, help_text='User progress at time of unlock')),
                ('achievement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_achievements', to='learning.achievement')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_achievements', to='auth.user')),
            ],
            options={
                'db_table': 'jac_user_achievements',
            },
        ),
        migrations.CreateModel(
            name='UserAssessmentResult',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('best_score', models.FloatField(default=0.0)),
                ('average_score', models.FloatField(default=0.0)),
                ('total_attempts', models.PositiveIntegerField(default=0)),
                ('passed_attempts', models.PositiveIntegerField(default=0)),
                ('total_time_spent', models.DurationField(default=0)),
                ('first_attempt_score', models.FloatField(null=True, blank=True)),
                ('last_attempt_score', models.FloatField(null=True, blank=True)),
                ('improvement_rate', models.FloatField(default=0.0)),
                ('first_attempt_date', models.DateTimeField(null=True, blank=True)),
                ('last_attempt_date', models.DateTimeField(null=True, blank=True)),
                ('passed_date', models.DateTimeField(null=True, blank=True)),
                ('is_completed', models.BooleanField(default=False)),
                ('completion_date', models.DateTimeField(null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('assessment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_results', to='learning.assessment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assessment_results', to='auth.user')),
            ],
            options={
                'db_table': 'jac_user_assessment_results',
            },
        ),
        migrations.AddIndex(
            model_name='assessmentattempt',
            index=models.Index(fields=['user', 'assessment'], name='jac_assess_user_id_assessment__31e7d8_idx'),
        ),
        migrations.AddIndex(
            model_name='assessmentattempt',
            index=models.Index(fields=['status', 'started_at'], name='jac_assess_status_started__22c6c6_idx'),
        ),
        migrations.AddIndex(
            model_name='assessmentattempt',
            index=models.Index(fields=['assessment', 'attempt_number'], name='jac_assess_assessmen_attempt__3b3b2a_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='assessmentattempt',
            unique_together={('user', 'assessment', 'attempt_number')},
        ),
        migrations.AddIndex(
            model_name='assessmentquestion',
            index=models.Index(fields=['assessment', 'order'], name='jac_assess_assessmen_order_c2bd15_idx'),
        ),
        migrations.AddIndex(
            model_name='assessmentquestion',
            index=models.Index(fields=['difficulty_level'], name='jac_assess_difficul_6e3c49_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='assessmentquestion',
            unique_together={('assessment', 'question')},
        ),
        migrations.AddIndex(
            model_name='achievement',
            index=models.Index(fields=['achievement_type'], name='jac_achie_achievem_e7c9b8_idx'),
        ),
        migrations.AddIndex(
            model_name='achievement',
            index=models.Index(fields=['rarity'], name='jac_achie_rarity_5f52e5_idx'),
        ),
        migrations.AddIndex(
            model_name='achievement',
            index=models.Index(fields=['is_active'], name='jac_achie_is_acti_d40c8e_idx'),
        ),
        migrations.AddIndex(
            model_name='userachievement',
            index=models.models.Index(fields=['user', 'unlocked_at'], name='jac_userac_user_id_unlocke_7aed4a_idx'),
        ),
        migrations.AddIndex(
            model_name='userachievement',
            index=models.Index(fields=['achievement'], name='jac_userac_achievem_a7a43b_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='userachievement',
            unique_together={('user', 'achievement')},
        ),
        migrations.AddIndex(
            model_name='userassessmentresult',
            index=models.Index(fields=['user', 'assessment'], name='jac_useras_user_id_assessm_7c84a1_idx'),
        ),
        migrations.AddIndex(
            model_name='userassessmentresult',
            index=models.Index(fields=['is_completed', 'best_score'], name='jac_useras_is_comp_be5c89_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='userassessmentresult',
            unique_together={('user', 'assessment')},
        ),
    ]
