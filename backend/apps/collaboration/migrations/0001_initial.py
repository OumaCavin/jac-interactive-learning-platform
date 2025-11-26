# JAC Interactive Learning Platform - Core backend implementation by Cavin Otieno

# Generated migration for collaboration features

from django.db import migrations, models
import uuid
from django.conf import settings
from django.db import models as django_models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('learning', '0003_adaptive_learning_clean'),  # Fixed dependency on learning app
    ]

    operations = [
        migrations.CreateModel(
            name='StudyGroup',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(db_index=True, max_length=200)),
                ('description', models.TextField(blank=True)),
                ('subject_area', models.CharField(db_index=True, max_length=100)),
                ('level', models.CharField(choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced'), ('expert', 'Expert')], max_length=50)),
                ('max_members', models.PositiveIntegerField(default=10)),
                ('is_public', models.BooleanField(default=True)),
                ('requires_approval', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', django_models.ForeignKey(on_delete=django_models.CASCADE, related_name='created_study_groups', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'collaboration_study_group',
            },
        ),
        migrations.CreateModel(
            name='StudyGroupMembership',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('role', models.CharField(choices=[('member', 'Member'), ('moderator', 'Moderator'), ('leader', 'Leader')], default='member', max_length=20)),
                ('joined_at', models.DateTimeField(auto_now_add=True)),
                ('study_group', django_models.ForeignKey(on_delete=django_models.CASCADE, related_name='memberships', to='collaboration.studygroup')),
                ('user', django_models.ForeignKey(on_delete=django_models.CASCADE, related_name='study_group_memberships', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'collaboration_study_group_membership',
            },
        ),
        migrations.CreateModel(
            name='DiscussionForum',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('study_group', django_models.OneToOneField(on_delete=django_models.CASCADE, related_name='forum', to='collaboration.studygroup')),
            ],
            options={
                'db_table': 'collaboration_discussion_forum',
            },
        ),
        migrations.CreateModel(
            name='DiscussionTopic',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(db_index=True, max_length=200)),
                ('content', models.TextField()),
                ('status', models.CharField(choices=[('open', 'Open'), ('closed', 'Closed'), ('pinned', 'Pinned')], default='open', max_length=20)),
                ('is_pinned', models.BooleanField(default=False)),
                ('views_count', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('author', django_models.ForeignKey(on_delete=django_models.CASCADE, related_name='created_topics', to=settings.AUTH_USER_MODEL)),
                ('forum', django_models.ForeignKey(on_delete=django_models.CASCADE, related_name='topics', to='collaboration.discussionforum')),
            ],
            options={
                'db_table': 'collaboration_discussion_topic',
            },
        ),
        migrations.CreateModel(
            name='DiscussionPost',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('content', models.TextField()),
                ('is_solution', models.BooleanField(default=False, help_text='Marked as solution by topic author')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('author', django_models.ForeignKey(on_delete=django_models.CASCADE, related_name='discussion_posts', to=settings.AUTH_USER_MODEL)),
                ('parent_post', django_models.ForeignKey(blank=True, null=True, on_delete=django_models.CASCADE, related_name='replies', to='collaboration.discussionpost')),
                ('topic', django_models.ForeignKey(on_delete=django_models.CASCADE, related_name='posts', to='collaboration.discussiontopic')),
            ],
            options={
                'db_table': 'collaboration_discussion_post',
            },
        ),
        migrations.CreateModel(
            name='PeerCodeShare',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(db_index=True, max_length=200)),
                ('description', models.TextField(blank=True)),
                ('code_content', models.TextField(help_text='Actual code content')),
                ('language', models.CharField(db_index=True, max_length=50)),
                ('file_name', models.CharField(blank=True, max_length=200)),
                ('tags', models.JSONField(default=list, help_text='List of tags for categorization')),
                ('share_type', models.CharField(choices=[('snippet', 'Code Snippet'), ('project', 'Full Project'), ('solution', 'Problem Solution'), ('tutorial', 'Tutorial')], max_length=20)),
                ('is_public', models.BooleanField(default=True)),
                ('is_tutorial', models.BooleanField(default=False)),
                ('likes_count', models.PositiveIntegerField(default=0)),
                ('downloads_count', models.PositiveIntegerField(default=0)),
                ('views_count', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('author', django_models.ForeignKey(on_delete=django_models.CASCADE, related_name='shared_codes', to=settings.AUTH_USER_MODEL)),
                ('study_group', django_models.ForeignKey(blank=True, null=True, on_delete=django_models.CASCADE, related_name='shared_codes', to='collaboration.studygroup')),
                ('topic', django_models.ForeignKey(blank=True, null=True, on_delete=django_models.CASCADE, related_name='shared_codes', to='collaboration.discussiontopic')),
            ],
            options={
                'db_table': 'collaboration_peer_code_share',
            },
        ),
        migrations.CreateModel(
            name='CodeLike',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('code_share', django_models.ForeignKey(on_delete=django_models.CASCADE, related_name='likes', to='collaboration.peercodeshare')),
                ('user', django_models.ForeignKey(on_delete=django_models.CASCADE, related_name='code_likes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'collaboration_code_like',
            },
        ),
        migrations.CreateModel(
            name='GroupChallenge',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(db_index=True, max_length=200)),
                ('description', models.TextField()),
                ('challenge_type', models.CharField(choices=[('coding', 'Coding Challenge'), ('problem_solving', 'Problem Solving'), ('research', 'Research Project'), ('presentation', 'Presentation')], max_length=30)),
                ('difficulty_level', models.CharField(choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard'), ('expert', 'Expert')], max_length=20)),
                ('problem_statement', models.TextField()),
                ('requirements', models.JSONField(default=list)),
                ('test_cases', models.JSONField(default=list)),
                ('solution_template', models.TextField(blank=True)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('estimated_duration', models.PositiveIntegerField(help_text='Estimated time in hours')),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('active', 'Active'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='draft', max_length=20)),
                ('max_participants', models.PositiveIntegerField(blank=True, null=True)),
                ('allow_team_participation', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', django_models.ForeignKey(on_delete=django_models.CASCADE, related_name='created_challenges', to=settings.AUTH_USER_MODEL)),
                ('study_group', django_models.ForeignKey(on_delete=django_models.CASCADE, related_name='challenges', to='collaboration.studygroup')),
            ],
            options={
                'db_table': 'collaboration_group_challenge',
            },
        ),
        migrations.CreateModel(
            name='ChallengeParticipation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('team_name', models.CharField(blank=True, max_length=200)),
                ('team_members', models.JSONField(default=list, help_text='List of team member usernames')),
                ('status', models.CharField(choices=[('registered', 'Registered'), ('in_progress', 'In Progress'), ('submitted', 'Submitted'), ('completed', 'Completed'), ('abandoned', 'Abandoned')], default='registered', max_length=20)),
                ('started_at', models.DateTimeField(blank=True, null=True)),
                ('submitted_at', models.DateTimeField(blank=True, null=True)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('submission_content', models.TextField(blank=True)),
                ('code_files', models.JSONField(default=list, help_text='List of submitted code files')),
                ('score', models.DecimalField(decimal_places=2, max_digits=5, null=True, blank=True)),
                ('feedback', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('challenge', django_models.ForeignKey(on_delete=django_models.CASCADE, related_name='participations', to='collaboration.groupchallenge')),
                ('participant', django_models.ForeignKey(on_delete=django_models.CASCADE, related_name='challenge_participations', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'collaboration_challenge_participation',
            },
        ),
        migrations.CreateModel(
            name='MentorshipRelationship',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('subject_areas', models.JSONField(default=list, help_text='Areas of expertise/interest')),
                ('goals', models.TextField(blank=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('active', 'Active'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='pending', max_length=20)),
                ('meeting_frequency', models.CharField(blank=True, help_text='e.g., weekly, bi-weekly', max_length=50)),
                ('session_duration', models.PositiveIntegerField(blank=True, help_text='Duration in minutes', null=True)),
                ('started_at', models.DateTimeField(blank=True, null=True)),
                ('ended_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('mentee', django_models.ForeignKey(on_delete=django_models.CASCADE, related_name='mentee_relationships', to=settings.AUTH_USER_MODEL)),
                ('mentor', django_models.ForeignKey(on_delete=django_models.CASCADE, related_name='mentoring_relationships', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'collaboration_mentorship_relationship',
            },
        ),
        migrations.CreateModel(
            name='MentorshipSession',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('agenda', models.TextField(blank=True)),
                ('notes', models.TextField(blank=True)),
                ('action_items', models.JSONField(default=list)),
                ('scheduled_start', models.DateTimeField()),
                ('scheduled_end', models.DateTimeField()),
                ('actual_start', models.DateTimeField(blank=True, null=True)),
                ('actual_end', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(choices=[('scheduled', 'Scheduled'), ('completed', 'Completed'), ('cancelled', 'Cancelled'), ('no_show', 'No Show')], default='scheduled', max_length=20)),
                ('session_type', models.CharField(choices=[('one_on_one', 'One-on-One'), ('group', 'Group Session'), ('code_review', 'Code Review'), ('project_discussion', 'Project Discussion')], default='one_on_one', max_length=50)),
                ('mentor_feedback', models.TextField(blank=True)),
                ('mentee_feedback', models.TextField(blank=True)),
                ('rating', models.PositiveIntegerField(blank=True, help_text='1-5 rating', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('relationship', django_models.ForeignKey(on_delete=django_models.CASCADE, related_name='sessions', to='collaboration.mentorshiprelationship')),
            ],
            options={
                'db_table': 'collaboration_mentorship_session',
            },
        ),
        migrations.AddConstraint(
            model_name='studygroupmembership',
            constraint=models.UniqueConstraint(fields=('study_group', 'user'), name='collaboration_study_group_m_user_unique'),
        ),
        migrations.AddConstraint(
            model_name='codelike',
            constraint=models.UniqueConstraint(fields=('code_share', 'user'), name='collaboration_code_like_code_share_user_unique'),
        ),
        migrations.AddConstraint(
            model_name='challengeparticipation',
            constraint=models.UniqueConstraint(fields=('challenge', 'participant'), name='collaboration_challenge_participation_challenge_participant_unique'),
        ),
        migrations.AddConstraint(
            model_name='mentorshiprelationship',
            constraint=models.UniqueConstraint(fields=('mentor', 'mentee'), name='collaboration_mentorship_relationship_mentor_mentee_unique'),
        ),
    ]