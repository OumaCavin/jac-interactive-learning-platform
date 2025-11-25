"""
Collaboration Serializers - JAC Learning Platform

Django REST Framework serializers for collaboration features.

Author: MiniMax Agent
Created: 2025-11-26
"""

from rest_framework import serializers
from django.contrib.auth.models import User
from django.utils import timezone
from .models import (
    StudyGroup, StudyGroupMembership, DiscussionForum, DiscussionTopic,
    DiscussionPost, PeerCodeShare, CodeLike, GroupChallenge,
    ChallengeParticipation, MentorshipRelationship, MentorshipSession
)

class UserBasicSerializer(serializers.ModelSerializer):
    """Basic user serializer for relationships"""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']
        read_only_fields = ['id']

class StudyGroupSerializer(serializers.ModelSerializer):
    """Serializer for StudyGroup model"""
    created_by = UserBasicSerializer(read_only=True)
    member_count = serializers.SerializerMethodField()
    is_member = serializers.SerializerMethodField()
    
    class Meta:
        model = StudyGroup
        fields = [
            'id', 'name', 'description', 'subject_area', 'level',
            'max_members', 'is_public', 'requires_approval', 'member_count',
            'is_member', 'created_by', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at', 'member_count', 'is_member']
    
    def get_member_count(self, obj):
        return obj.memberships.count()
    
    def get_is_member(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.memberships.filter(user=request.user).exists()
        return False

class StudyGroupMembershipSerializer(serializers.ModelSerializer):
    """Serializer for StudyGroupMembership model"""
    study_group = StudyGroupSerializer(read_only=True)
    user = UserBasicSerializer(read_only=True)
    
    class Meta:
        model = StudyGroupMembership
        fields = ['id', 'study_group', 'user', 'role', 'joined_at']
        read_only_fields = ['id', 'joined_at']

class DiscussionTopicSerializer(serializers.ModelSerializer):
    """Serializer for DiscussionTopic model"""
    author = UserBasicSerializer(read_only=True)
    forum = serializers.StringRelatedField(read_only=True)
    posts_count = serializers.SerializerMethodField()
    
    class Meta:
        model = DiscussionTopic
        fields = [
            'id', 'forum', 'title', 'content', 'author', 'status',
            'is_pinned', 'views_count', 'posts_count', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'author', 'views_count', 'created_at', 'updated_at', 'posts_count'
        ]
    
    def get_posts_count(self, obj):
        return obj.posts.count()

class DiscussionPostSerializer(serializers.ModelSerializer):
    """Serializer for DiscussionPost model"""
    author = UserBasicSerializer(read_only=True)
    topic = DiscussionTopicSerializer(read_only=True)
    parent_post = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = DiscussionPost
        fields = [
            'id', 'topic', 'author', 'content', 'parent_post',
            'is_solution', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']

class PeerCodeShareSerializer(serializers.ModelSerializer):
    """Serializer for PeerCodeShare model"""
    author = UserBasicSerializer(read_only=True)
    topic = DiscussionTopicSerializer(read_only=True)
    study_group = StudyGroupSerializer(read_only=True)
    is_liked = serializers.SerializerMethodField()
    
    class Meta:
        model = PeerCodeShare
        fields = [
            'id', 'title', 'description', 'code_content', 'language',
            'file_name', 'tags', 'share_type', 'is_public', 'is_tutorial',
            'likes_count', 'downloads_count', 'views_count', 'is_liked',
            'author', 'topic', 'study_group', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'author', 'likes_count', 'downloads_count', 'views_count',
            'created_at', 'updated_at', 'is_liked'
        ]
    
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False

class CodeLikeSerializer(serializers.ModelSerializer):
    """Serializer for CodeLike model"""
    code_share = PeerCodeShareSerializer(read_only=True)
    user = UserBasicSerializer(read_only=True)
    
    class Meta:
        model = CodeLike
        fields = ['id', 'code_share', 'user', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']

class GroupChallengeSerializer(serializers.ModelSerializer):
    """Serializer for GroupChallenge model"""
    created_by = UserBasicSerializer(read_only=True)
    study_group = StudyGroupSerializer(read_only=True)
    participant_count = serializers.SerializerMethodField()
    is_participating = serializers.SerializerMethodField()
    
    class Meta:
        model = GroupChallenge
        fields = [
            'id', 'title', 'description', 'challenge_type', 'difficulty_level',
            'problem_statement', 'requirements', 'test_cases', 'solution_template',
            'start_date', 'end_date', 'estimated_duration', 'status',
            'max_participants', 'allow_team_participation', 'participant_count',
            'is_participating', 'created_by', 'study_group', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'created_by', 'created_at', 'updated_at', 'participant_count', 'is_participating'
        ]
    
    def get_participant_count(self, obj):
        return obj.participations.count()
    
    def get_is_participating(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.participations.filter(participant=request.user).exists()
        return False

class ChallengeParticipationSerializer(serializers.ModelSerializer):
    """Serializer for ChallengeParticipation model"""
    challenge = GroupChallengeSerializer(read_only=True)
    participant = UserBasicSerializer(read_only=True)
    
    class Meta:
        model = ChallengeParticipation
        fields = [
            'id', 'challenge', 'participant', 'team_name', 'team_members',
            'status', 'started_at', 'submitted_at', 'completed_at',
            'submission_content', 'code_files', 'score', 'feedback',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'participant', 'created_at', 'updated_at',
            'started_at', 'submitted_at', 'completed_at'
        ]

class MentorshipRelationshipSerializer(serializers.ModelSerializer):
    """Serializer for MentorshipRelationship model"""
    mentor = UserBasicSerializer(read_only=True)
    mentee = UserBasicSerializer(read_only=True)
    
    class Meta:
        model = MentorshipRelationship
        fields = [
            'id', 'mentor', 'mentee', 'subject_areas', 'goals',
            'status', 'meeting_frequency', 'session_duration',
            'started_at', 'ended_at', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'mentor', 'started_at', 'ended_at', 'created_at', 'updated_at'
        ]

class MentorshipSessionSerializer(serializers.ModelSerializer):
    """Serializer for MentorshipSession model"""
    relationship = MentorshipRelationshipSerializer(read_only=True)
    
    class Meta:
        model = MentorshipSession
        fields = [
            'id', 'relationship', 'title', 'agenda', 'notes',
            'action_items', 'scheduled_start', 'scheduled_end',
            'actual_start', 'actual_end', 'status', 'session_type',
            'mentor_feedback', 'mentee_feedback', 'rating',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'actual_start', 'actual_end', 'created_at', 'updated_at'
        ]

# List serializers for dropdown/selection fields
class StudyGroupListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for study group lists"""
    member_count = serializers.SerializerMethodField()
    
    class Meta:
        model = StudyGroup
        fields = ['id', 'name', 'subject_area', 'level', 'member_count']
    
    def get_member_count(self, obj):
        return obj.memberships.count()

class UserListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for user lists"""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']

# Summary serializers
class CollaborationOverviewSerializer(serializers.Serializer):
    """Overview serializer for collaboration dashboard"""
    
    total_study_groups = serializers.IntegerField()
    active_discussions = serializers.IntegerField()
    code_shares = serializers.IntegerField()
    active_challenges = serializers.IntegerField()
    active_mentorships = serializers.IntegerField()
    my_study_groups = serializers.IntegerField()
    my_posts = serializers.IntegerField()
    my_code_shares = serializers.IntegerField()