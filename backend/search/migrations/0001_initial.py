# Generated migration for search app

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SearchQuery',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('query', models.CharField(max_length=255)),
                ('results_count', models.PositiveIntegerField(default=0)),
                ('clicked_result', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=models.deletion.CASCADE, related_name='search_queries', to='users.user')),
            ],
            options={
                'verbose_name': 'Search Query',
                'verbose_name_plural': 'Search Queries',
                'db_table': 'search_queries',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='SearchResult',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('query', models.CharField(max_length=255)),
                ('content_type', models.CharField(choices=[('learning_path', 'Learning Path'), ('module', 'Module'), ('lesson', 'Lesson'), ('assessment', 'Assessment'), ('knowledge_node', 'Knowledge Node'), ('content', 'Content'), ('user', 'User')], max_length=20)),
                ('content_id', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('url', models.CharField(max_length=500)),
                ('tags', models.JSONField(default=list)),
                ('relevance_score', models.FloatField(default=0.0)),
                ('popularity_score', models.FloatField(default=0.0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Search Result',
                'verbose_name_plural': 'Search Results',
                'db_table': 'search_results',
                'ordering': ['-relevance_score', '-popularity_score'],
            },
        ),
        migrations.AddIndex(
            model_name='searchquery',
            index=models.Index(fields=['query'], name='search_queries_query_idx'),
        ),
        migrations.AddIndex(
            model_name='searchquery',
            index=models.Index(fields=['created_at'], name='search_queries_created_idx'),
        ),
        migrations.AddIndex(
            model_name='searchresult',
            index=models.Index(fields=['content_type'], name='search_results_content_idx'),
        ),
        migrations.AddIndex(
            model_name='searchresult',
            index=models.Index(fields=['query'], name='search_results_query_idx'),
        ),
    ]