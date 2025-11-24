# Generated migration for Knowledge Graph app

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils import timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ConceptRelation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('concept_a', models.CharField(max_length=200)),
                ('concept_b', models.CharField(max_length=200)),
                ('relation_type', models.CharField(choices=[('inherits', 'Inheritance - Concept A inherits from B'), ('implements', 'Implementation - A implements B'), ('depends', 'Dependency - A depends on B'), ('conflicts', 'Conflict - A conflicts with B'), ('complements', 'Complement - A complements B'), ('alternatives', 'Alternative - A is alternative to B')], max_length=20)),
                ('domain', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('confidence_score', models.FloatField(default=0.8, help_text='Confidence score for this relationship (0.0 to 1.0)', validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.0)])),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(default=timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'concept_relation',
                'ordering': ['domain', 'relation_type', 'concept_a'],
            },
        ),
        migrations.CreateModel(
            name='KnowledgeEdge',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('edge_type', models.CharField(choices=[('prerequisite', 'Prerequisite - Must learn before'), ('related', 'Related - Connected concepts'), ('example', 'Example - Shows application of'), ('depends_on', 'Depends On - Requires understanding of'), ('leads_to', 'Leads To - Next logical step'), ('contradicts', 'Contradicts - Opposite concepts'), ('similar_to', 'Similar To - Related concepts'), ('part_of', 'Part Of - Component of larger concept'), ('contains', 'Contains - Includes sub-concepts')], max_length=20)),
                ('strength', models.CharField(choices=[('weak', 'Weak Connection'), ('moderate', 'Moderate Connection'), ('strong', 'Strong Connection'), ('essential', 'Essential Connection')], default='moderate', max_length=20)),
                ('curve_points', models.JSONField(default=list, help_text='Control points for curved edges')),
                ('edge_weight', models.FloatField(default=1.0, help_text='Numerical weight for pathfinding algorithms')),
                ('description', models.TextField(blank=True, help_text='Description of the relationship')),
                ('examples', models.JSONField(default=list, blank=True, help_text='Examples illustrating this relationship')),
                ('traversal_count', models.IntegerField(default=0, help_text='Number of times this edge has been traversed')),
                ('created_at', models.DateTimeField(default=timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'knowledge_edge',
                'ordering': ['-traversal_count', 'edge_type'],
            },
        ),
        migrations.CreateModel(
            name='KnowledgeNode',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('node_type', models.CharField(choices=[('concept', 'Concept'), ('skill', 'Skill'), ('topic', 'Topic'), ('objective', 'Learning Objective'), ('assessment', 'Assessment'), ('resource', 'Learning Resource')], max_length=20)),
                ('difficulty_level', models.CharField(choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced'), ('expert', 'Expert')], default='beginner', max_length=20)),
                ('x_position', models.FloatField(default=0.0)),
                ('y_position', models.FloatField(default=0.0)),
                ('z_position', models.FloatField(default=0.0)),
                ('width', models.FloatField(default=1.0)),
                ('height', models.FloatField(default=1.0)),
                ('content_uri', models.CharField(blank=True, max_length=500)),
                ('jac_code', models.TextField(blank=True)),
                ('learning_objectives', models.JSONField(default=list, help_text='List of learning objectives')),
                ('prerequisites', models.JSONField(default=list, help_text='Required prior knowledge')),
                ('created_at', models.DateTimeField(default=timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('view_count', models.IntegerField(default=0)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'knowledge_node',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='LearningGraph',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('graph_type', models.CharField(choices=[('course', 'Complete Course Curriculum'), ('module', 'Learning Module'), ('topic', 'Topic-Specific Graph'), ('skill_tree', 'Skill Development Tree'), ('concept_map', 'Concept Relationship Map'), ('assessment_path', 'Assessment Preparation Path')], max_length=20)),
                ('status', models.CharField(choices=[('draft', 'Draft - Under Development'), ('active', 'Active - Available for Learning'), ('archived', 'Archived - No Longer Active'), ('review', 'In Review - Being Evaluated')], default='draft', max_length=20)),
                ('subject_area', models.CharField(max_length=100)),
                ('target_audience', models.CharField(max_length=100)),
                ('estimated_duration', models.DurationField(blank=True, null=True)),
                ('layout_config', models.JSONField(default=dict, help_text='Configuration for graph visualization layout')),
                ('view_box', models.JSONField(default=dict, help_text='View box coordinates for graph display')),
                ('adaptive_rules', models.JSONField(default=dict, help_text='Rules for adaptive path generation')),
                ('difficulty_progression', models.JSONField(default=list, help_text='Configured difficulty progression path')),
                ('completion_rate', models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.0)])),
                ('average_completion_time', models.DurationField(blank=True, null=True)),
                ('total_attempts', models.IntegerField(default=0)),
                ('successful_completions', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(default=timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('version', models.CharField(default='1.0.0', max_length=20)),
                ('tags', models.JSONField(default=list, help_text='Tags for categorization and search')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'learning_graph',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='LearningPath',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('adaptation_type', models.CharField(choices=[('static', 'Static - Fixed Path'), ('adaptive', 'Adaptive - Adjusts Based on Performance'), ('personalized', 'Personalized - Based on User Profile'), ('ai_generated', 'AI Generated - ML-Optimized')], default='adaptive', max_length=20)),
                ('status', models.CharField(choices=[('active', 'Active - Currently Following'), ('completed', 'Completed Successfully'), ('paused', 'Paused - Temporarily Stopped'), ('abandoned', 'Abandoned - No Longer Following'), ('failed', 'Failed - Unable to Complete')], default='active', max_length=20)),
                ('completed_nodes', models.JSONField(default=list)),
                ('progress_percentage', models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(100.0)])),
                ('started_at', models.DateTimeField(default=timezone.now)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('last_activity', models.DateTimeField(default=timezone.now)),
                ('total_time_spent', models.DurationField(default=timezone.timedelta)),
                ('performance_metrics', models.JSONField(default=dict)),
                ('adaptation_history', models.JSONField(default=list)),
                ('current_node', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='knowledge_graph.knowledgenode')),
                ('learning_graph', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='knowledge_graph.learninggraph')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'learning_path',
                'ordering': ['-last_activity'],
            },
        ),
        migrations.CreateModel(
            name='UserKnowledgeState',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('mastery_level', models.CharField(choices=[('novice', 'Novice - No Understanding'), ('beginner', 'Beginner - Basic Awareness'), ('developing', 'Developing - Growing Understanding'), ('proficient', 'Proficient - Good Understanding'), ('expert', 'Expert - Deep Understanding')], default='novice', max_length=20)),
                ('confidence_score', models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.0)])),
                ('first_exposure', models.DateTimeField(default=timezone.now)),
                ('last_reviewed', models.DateTimeField(default=timezone.now)),
                ('total_time_spent', models.DurationField(default=timezone.timedelta)),
                ('assessment_scores', models.JSONField(default=list)),
                ('practice_attempts', models.IntegerField(default=0)),
                ('successful_attempts', models.IntegerField(default=0)),
                ('next_review_date', models.DateTimeField(blank=True, null=True)),
                ('review_interval', models.DurationField(default=timezone.timedelta)),
                ('learning_velocity', models.FloatField(default=0.0)),
                ('difficulty_adjustment', models.FloatField(default=0.0)),
                ('knowledge_node', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='knowledge_graph.knowledgenode')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_knowledge_state',
                'ordering': ['user', 'knowledge_node__title'],
            },
        ),
        migrations.AddField(
            model_name='knowledgeedge',
            name='source_node',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='outgoing_edges', to='knowledge_graph.knowledgenode'),
        ),
        migrations.AddField(
            model_name='knowledgeedge',
            name='target_node',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='incoming_edges', to='knowledge_graph.knowledgenode'),
        ),
        migrations.CreateModel(
            name='LearningGraphNode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display_order', models.IntegerField(default=0)),
                ('is_mandatory', models.BooleanField(default=True)),
                ('node_weight', models.FloatField(default=1.0)),
                ('custom_x', models.FloatField(blank=True, null=True)),
                ('custom_y', models.FloatField(blank=True, null=True)),
                ('estimated_time', models.DurationField(blank=True, null=True)),
                ('prerequisite_score', models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.0)])),
                ('knowledge_node', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='knowledge_graph.knowledgenode')),
                ('learning_graph', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='knowledge_graph.learninggraph')),
            ],
            options={
                'db_table': 'learning_graph_node',
                'ordering': ['display_order', 'knowledge_node__title'],
            },
        ),
        migrations.CreateModel(
            name='LearningGraphEdge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display_order', models.IntegerField(default=0)),
                ('is_mandatory', models.BooleanField(default=False)),
                ('edge_priority', models.IntegerField(default=1)),
                ('unlock_conditions', models.JSONField(default=dict)),
                ('recommended_for', models.JSONField(default=list)),
                ('custom_path', models.JSONField(default=list)),
                ('knowledge_edge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='knowledge_graph.knowledgeedge')),
                ('learning_graph', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='knowledge_graph.learninggraph')),
            ],
            options={
                'db_table': 'learning_graph_edge',
                'ordering': ['display_order', 'edge_priority'],
            },
        ),
        migrations.AddField(
            model_name='learninggraph',
            name='edges',
            field=models.ManyToManyField(blank=True, through='knowledge_graph.LearningGraphEdge', to='knowledge_graph.knowledgeedge'),
        ),
        migrations.AddField(
            model_name='learninggraph',
            name='nodes',
            field=models.ManyToManyField(blank=True, through='knowledge_graph.LearningGraphNode', to='knowledge_graph.knowledgenode'),
        ),
        migrations.AddField(
            model_name='conceptrelation',
            name='related_nodes',
            field=models.ManyToManyField(blank=True, to='knowledge_graph.knowledgenode'),
        ),
        migrations.AlterUniqueTogether(
            name='knowledgeedge',
            unique_together={('source_node', 'target_node', 'edge_type')},
        ),
        migrations.AlterUniqueTogether(
            name='learninggraphnode',
            unique_together={('learning_graph', 'knowledge_node')},
        ),
        migrations.AlterUniqueTogether(
            name='learninggraphedge',
            unique_together={('learning_graph', 'knowledge_edge')},
        ),
        migrations.AlterUniqueTogether(
            name='conceptrelation',
            unique_together={('concept_a', 'concept_b', 'relation_type', 'domain')},
        ),
        migrations.AlterUniqueTogether(
            name='userknowledgestate',
            unique_together={('user', 'knowledge_node')},
        ),
    ]