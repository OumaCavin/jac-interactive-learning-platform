# Generated migration for gamification app

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Achievement',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200, unique=True)),
                ('description', models.TextField()),
                ('icon', models.CharField(max_length=100)),
                ('category', models.CharField(choices=[('completion', 'Completion'), ('effort', 'Effort'), ('skill', 'Skill'), ('assessment', 'Assessment'), ('consistency', 'Consistency'), ('collaboration', 'Collaboration'), ('milestone', 'Milestone'), ('special', 'Special')], max_length=20)),
                ('difficulty', models.CharField(choices=[('bronze', 'Bronze'), ('silver', 'Silver'), ('gold', 'Gold'), ('platinum', 'Platinum'), ('diamond', 'Diamond')], default='bronze', max_length=15)),
                ('criteria_type', models.CharField(max_length=50)),
                ('criteria_value', models.PositiveIntegerField()),
                ('criteria_operator', models.CharField(choices=[('gte', 'Greater than or equal'), ('gt', 'Greater than'), ('eq', 'Equal')], default='gte', max_length=10)),
                ('points_reward', models.PositiveIntegerField(default=10)),
                ('is_active', models.BooleanField(default=True)),
                ('unlock_order', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'gamification_achievement',
                'ordering': ['category', 'difficulty', 'unlock_order', 'title'],
            },
        ),
        migrations.CreateModel(
            name='AchievementProgress',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('current_count', models.PositiveIntegerField(default=0)),
                ('target_count', models.PositiveIntegerField()),
                ('last_update', models.DateTimeField(default=django.utils.timezone.now)),
                ('context_data', models.JSONField(blank=True, default=dict)),
                ('achievement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_tracking', to='gamification.achievement')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='achievement_progress', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'achievement_progress',
                'ordering': ['-last_update'],
            },
        ),
        migrations.CreateModel(
            name='Badge',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('description', models.TextField()),
                ('icon', models.CharField(max_length=100)),
                ('category', models.CharField(choices=[('learning', 'Learning'), ('coding', 'Coding'), ('assessment', 'Assessment'), ('engagement', 'Engagement'), ('consistency', 'Consistency'), ('milestone', 'Milestone'), ('special', 'Special')], max_length=20)),
                ('difficulty', models.CharField(choices=[('bronze', 'Bronze'), ('silver', 'Silver'), ('gold', 'Gold'), ('platinum', 'Platinum'), ('diamond', 'Diamond')], default='bronze', max_length=15)),
                ('requirements', models.JSONField(default=dict)),
                ('minimum_points', models.PositiveIntegerField(default=0)),
                ('unlock_conditions', models.JSONField(blank=True, default=dict)),
                ('is_active', models.BooleanField(default=True)),
                ('rarity', models.CharField(choices=[('common', 'Common'), ('rare', 'Rare'), ('epic', 'Epic'), ('legendary', 'Legendary')], default='common', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'badge',
                'ordering': ['category', 'difficulty', 'name'],
            },
        ),
        migrations.CreateModel(
            name='LevelRequirement',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('level', models.PositiveIntegerField(unique=True)),
                ('requirement_type', models.CharField(choices=[('points', 'Points'), ('xp', 'Experience Points'), ('achievements', 'Achievements Count'), ('modules', 'Modules Completed'), ('assessments', 'Assessments Completed'), ('streak', 'Learning Streak')], max_length=20)),
                ('requirement_value', models.PositiveIntegerField()),
                ('title', models.CharField(blank=True, max_length=100)),
                ('description', models.TextField(blank=True)),
                ('unlock_features', models.JSONField(blank=True, default=list)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('badge', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gamification.badge')),
            ],
            options={
                'db_table': 'level_requirement',
                'ordering': ['level'],
            },
        ),
        migrations.CreateModel(
            name='LearningStreak',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('current_streak', models.PositiveIntegerField(default=0)),
                ('longest_streak', models.PositiveIntegerField(default=0)),
                ('last_activity_date', models.DateField(blank=True, null=True)),
                ('streak_history', models.JSONField(blank=True, default=list)),
                ('streak_breaks', models.JSONField(blank=True, default=list)),
                ('streak_multiplier', models.FloatField(default=1.0, validators=[django.core.validators.MinValueValidator(1.0), django.core.validators.MaxValueValidator(3.0)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='learning_streaks', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'learning_streak',
                'ordering': ['-current_streak'],
            },
        ),
        migrations.CreateModel(
            name='PointTransaction',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('amount', models.IntegerField()),
                ('transaction_type', models.CharField(choices=[('earned', 'Earned'), ('spent', 'Spent'), ('bonus', 'Bonus'), ('penalty', 'Penalty')], max_length=15)),
                ('source', models.CharField(max_length=50)),
                ('description', models.CharField(blank=True, max_length=200)),
                ('metadata', models.JSONField(blank=True, default=dict)),
                ('balance_after', models.PositiveIntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='point_transactions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'point_transaction',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='UserAchievement',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('current_progress', models.PositiveIntegerField(default=0)),
                ('target_progress', models.PositiveIntegerField()),
                ('progress_percentage', models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(100.0)])),
                ('is_completed', models.BooleanField(default=False)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('started_at', models.DateTimeField(auto_now_add=True)),
                ('points_earned', models.PositiveIntegerField(default=0)),
                ('progress_history', models.JSONField(blank=True, default=list)),
                ('last_progress_update', models.DateTimeField(default=django.utils.timezone.now)),
                ('achievement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_progress', to='gamification.achievement')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_achievements', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_achievement',
                'ordering': ['-last_progress_update'],
            },
        ),
        migrations.CreateModel(
            name='UserBadge',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('earned_at', models.DateTimeField(auto_now_add=True)),
                ('progress_data', models.JSONField(blank=True, default=dict)),
                ('earned_through', models.CharField(blank=True, max_length=100)),
                ('is_verified', models.BooleanField(default=True)),
                ('verified_at', models.DateTimeField(blank=True, null=True)),
                ('badge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_owners', to='gamification.badge')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_badges', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_badge',
                'ordering': ['-earned_at'],
            },
        ),
        migrations.CreateModel(
            name='UserLevel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('current_level', models.PositiveIntegerField(default=1)),
                ('current_xp', models.PositiveIntegerField(default=0)),
                ('total_xp', models.PositiveIntegerField(default=0)),
                ('xp_to_next_level', models.PositiveIntegerField()),
                ('level_up_notifications', models.JSONField(blank=True, default=list)),
                ('last_level_up', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_levels', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_level',
                'ordering': ['-total_xp'],
            },
        ),
        migrations.CreateModel(
            name='UserPoints',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('total_points', models.PositiveIntegerField(default=0)),
                ('available_points', models.PositiveIntegerField(default=0)),
                ('lifetime_points', models.PositiveIntegerField(default=0)),
                ('learning_points', models.PositiveIntegerField(default=0)),
                ('coding_points', models.PositiveIntegerField(default=0)),
                ('assessment_points', models.PositiveIntegerField(default=0)),
                ('engagement_points', models.PositiveIntegerField(default=0)),
                ('last_earned', models.DateTimeField(blank=True, null=True)),
                ('last_spent', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_points', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_points',
                'ordering': ['-total_points'],
            },
        ),
        migrations.AddField(
            model_name='achievement',
            name='badge',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='achievements', to='gamification.badge'),
        ),
        migrations.AddField(
            model_name='userachievement',
            name='badge_earned',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gamification.userbadge'),
        ),
        migrations.AlterUniqueTogether(
            name='userbadge',
            unique_together={('user', 'badge')},
        ),
        migrations.AlterUniqueTogether(
            name='userachievement',
            unique_together={('user', 'achievement')},
        ),
        migrations.AlterUniqueTogether(
            name='userpoints',
            unique_together={('user',)},
        ),
        migrations.AlterUniqueTogether(
            name='userlevel',
            unique_together={('user',)},
        ),
        migrations.AlterUniqueTogether(
            name='learningstreak',
            unique_together={('user',)},
        ),
        migrations.AlterUniqueTogether(
            name='achievementprogress',
            unique_together={('user', 'achievement')},
        ),
    ]