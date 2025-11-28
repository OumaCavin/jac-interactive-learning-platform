# JAC Interactive Learning Platform - Core backend implementation by Cavin Otieno

# Migration to fix collaboration app conflicts and missing constraints

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('collaboration', '0001_initial'),
    ]

    operations = [
        # Add missing constraints that match model definitions
        migrations.AddConstraint(
            model_name='discussiontopic',
            constraint=models.UniqueConstraint(fields=('forum', 'title'), name='collaboration_discussion_topic_forum_title_unique'),
        ),
        
        # Add ordering constraints via indexes (simulating model ordering)
        migrations.AddIndex(
            model_name='studygroup',
            index=models.Index(fields=['-created_at'], name='collaboration_study_group_created_at_idx'),
        ),
        
        migrations.AddIndex(
            model_name='challengeparticipation',
            index=models.Index(fields=['-created_at'], name='collaboration_challenge_participation_created_at_idx'),
        ),
        
        migrations.AddIndex(
            model_name='mentorshiprelationship',
            index=models.Index(fields=['-created_at'], name='collaboration_mentorship_relationship_created_at_idx'),
        ),
        
        # Add unique constraint for DiscussionPost to prevent duplicate posts by same user in same topic at same time
        migrations.AddConstraint(
            model_name='discussionpost',
            constraint=models.UniqueConstraint(fields=('topic', 'author'), name='collaboration_discussion_post_topic_author_unique'),
        ),
        
        # Ensure foreign key relationships are properly defined
        migrations.AlterField(
            model_name='discussiontopic',
            name='forum',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topics', to='collaboration.discussionforum'),
        ),
    ]