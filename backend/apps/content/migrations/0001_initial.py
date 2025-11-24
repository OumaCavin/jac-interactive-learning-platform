"""
Migration for content app
"""

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('learning', '0003_alter_assessmentattempt_module_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Content',
            fields=[
                ('content_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('content_type', models.CharField(choices=[('markdown', 'Markdown'), ('html', 'HTML'), ('interactive', 'Interactive Content'), ('video', 'Video'), ('document', 'Document'), ('code_tutorial', 'Code Tutorial'), ('exercise', 'Exercise')], default='markdown', max_length=20)),
                ('difficulty_level', models.CharField(choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')], default='beginner', max_length=20)),
                ('content_data', models.JSONField(default=dict)),
                ('estimated_duration', models.PositiveIntegerField(default=30)),
                ('tags', models.JSONField(default=list)),
                ('topic', models.CharField(blank=True, max_length=100)),
                ('quality_rating', models.FloatField(blank=True, null=True, validators=[models.MinValueValidator(1.0), models.MaxValueValidator(5.0)])),
                ('learning_path', models.ForeignKey(blank=True, null=True, on_delete=models.CASCADE, related_name='content_items', to='learning.learningpath')),
                ('module', models.ForeignKey(blank=True, help_text='Primary module using this content', null=True, on_delete=models.CASCADE, related_name='content_items', to='learning.module')),
                ('is_published', models.BooleanField(default=False)),
                ('is_featured', models.BooleanField(default=False)),
                ('created_by', models.ForeignKey(on_delete=models.CASCADE, related_name='created_content', to='users.user')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Content',
                'verbose_name_plural': 'Content',
                'db_table': 'learning_content',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='ContentAnalytics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_views', models.PositiveIntegerField(default=0)),
                ('unique_viewers', models.PositiveIntegerField(default=0)),
                ('total_time_spent', models.DurationField(default=0)),
                ('average_completion_rate', models.FloatField(default=0.0)),
                ('total_clicks', models.PositiveIntegerField(default=0)),
                ('total_shares', models.PositiveIntegerField(default=0)),
                ('total_ratings', models.PositiveIntegerField(default=0)),
                ('average_rating', models.FloatField(default=0.0)),
                ('bounce_rate', models.FloatField(default=0.0)),
                ('return_visit_rate', models.FloatField(default=0.0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('content', models.OneToOneField(on_delete=models.CASCADE, related_name='analytics', to='content.content')),
            ],
            options={
                'verbose_name': 'Content Analytics',
                'verbose_name_plural': 'Content Analytics',
                'db_table': 'content_analytics',
            },
        ),
        migrations.CreateModel(
            name='ContentRecommendation',
            fields=[
                ('recommendation_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('recommendation_type', models.CharField(choices=[('personalized', 'Personalized'), ('based_on_progress', 'Progress-based'), ('similar_users', 'Similar users'), ('trending', 'Trending')], default='personalized', max_length=20)),
                ('match_score', models.FloatField(help_text='Match score from 0.0 to 1.0', validators=[models.MinValueValidator(0.0), models.MaxValueValidator(1.0)])),
                ('reasoning', models.JSONField(default=dict)),
                ('is_viewed', models.BooleanField(default=False)),
                ('is_dismissed', models.BooleanField(default=False)),
                ('clicked_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('expires_at', models.DateTimeField(blank=True, null=True)),
                ('content', models.ForeignKey(on_delete=models.CASCADE, related_name='recommendations', to='content.content')),
                ('user', models.ForeignKey(on_delete=models.CASCADE, related_name='content_recommendations', to='users.user')),
            ],
            options={
                'verbose_name': 'Content Recommendation',
                'verbose_name_plural': 'Content Recommendations',
                'db_table': 'content_recommendations',
                'ordering': ['-match_score', '-created_at'],
            },
        ),
        migrations.AddIndex(
            model_name='content',
            index=models.Index(fields=['content_type'], name='content_type_idx'),
        ),
        migrations.AddIndex(
            model_name='content',
            index=models.Index(fields=['difficulty_level'], name='difficulty_level_idx'),
        ),
        migrations.AddIndex(
            model_name='content',
            index=models.Index(fields=['is_published'], name='is_published_idx'),
        ),
        migrations.AddIndex(
            model_name='content',
            index=models.Index(fields=['topic'], name='topic_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='contentrecommendation',
            unique_together={('user', 'content', 'recommendation_type')},
        ),
    ]