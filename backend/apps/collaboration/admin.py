# JAC Interactive Learning Platform - Core backend implementation by Cavin Otieno

"""
Collaboration Admin - JAC Learning Platform

Django admin interfaces for collaboration features.

Author: Cavin Otieno
Created: 2025-11-26
"""

from django.contrib import admin
from config.custom_admin import custom_admin_site
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
from config.custom_admin import custom_admin_site
    StudyGroup, StudyGroupMembership, DiscussionForum, DiscussionTopic,
    DiscussionPost, PeerCodeShare, CodeLike, GroupChallenge,
    ChallengeParticipation, MentorshipRelationship, MentorshipSession
)

@admin.register(StudyGroup, site=custom_admin_site)
class StudyGroupAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'subject_area', 'level', 'member_count', 'is_public', 
        'created_by', 'created_at'
    ]
    list_filter = ['subject_area', 'level', 'is_public', 'created_at']
    search_fields = ['name', 'description', 'subject_area']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    def member_count(self, obj):
        return obj.memberships.count()
    member_count.short_description = 'Members'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('created_by').prefetch_related('memberships')

@admin.register(StudyGroupMembership, site=custom_admin_site)
class StudyGroupMembershipAdmin(admin.ModelAdmin):
    list_display = ['user', 'study_group', 'role', 'joined_at']
    list_filter = ['role', 'joined_at']
    search_fields = ['user__username', 'study_group__name']
    readonly_fields = ['joined_at']

@admin.register(DiscussionForum, site=custom_admin_site)
class DiscussionForumAdmin(admin.ModelAdmin):
    list_display = ['name', 'study_group', 'topic_count', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description', 'study_group__name']
    readonly_fields = ['created_at']
    
    def topic_count(self, obj):
        return obj.topics.count()
    topic_count.short_description = 'Topics'

@admin.register(DiscussionTopic, site=custom_admin_site)
class DiscussionTopicAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'forum', 'author', 'status', 'is_pinned', 
        'posts_count', 'views_count', 'created_at'
    ]
    list_filter = ['status', 'is_pinned', 'created_at']
    search_fields = ['title', 'content', 'author__username']
    readonly_fields = ['views_count', 'created_at', 'updated_at']
    
    def posts_count(self, obj):
        return obj.posts.count()
    posts_count.short_description = 'Posts'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('forum', 'forum__study_group', 'author').prefetch_related('posts')

@admin.register(DiscussionPost, site=custom_admin_site)
class DiscussionPostAdmin(admin.ModelAdmin):
    list_display = [
        'author', 'topic', 'is_solution', 'created_at', 'updated_at'
    ]
    list_filter = ['is_solution', 'created_at']
    search_fields = ['content', 'author__username', 'topic__title']
    readonly_fields = ['created_at', 'updated_at']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('author', 'topic', 'topic__forum', 'topic__forum__study_group')

@admin.register(PeerCodeShare, site=custom_admin_site)
class PeerCodeShareAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'author', 'language', 'share_type', 'likes_count', 
        'views_count', 'is_public', 'created_at'
    ]
    list_filter = ['language', 'share_type', 'is_public', 'created_at']
    search_fields = ['title', 'description', 'author__username']
    readonly_fields = [
        'likes_count', 'downloads_count', 'views_count', 
        'created_at', 'updated_at'
    ]
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('author').prefetch_related('likes')

@admin.register(CodeLike, site=custom_admin_site)
class CodeLikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'code_share', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'code_share__title']
    readonly_fields = ['created_at']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user', 'code_share', 'code_share__author')

@admin.register(GroupChallenge, site=custom_admin_site)
class GroupChallengeAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'study_group', 'challenge_type', 'difficulty_level',
        'status', 'participant_count', 'created_by', 'start_date'
    ]
    list_filter = [
        'challenge_type', 'difficulty_level', 'status', 
        'start_date', 'created_at'
    ]
    search_fields = ['title', 'description', 'study_group__name']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'start_date'
    
    def participant_count(self, obj):
        return obj.participations.count()
    participant_count.short_description = 'Participants'

@admin.register(ChallengeParticipation, site=custom_admin_site)
class ChallengeParticipationAdmin(admin.ModelAdmin):
    list_display = [
        'participant', 'challenge', 'status', 'team_name', 
        'submitted_at', 'score', 'created_at'
    ]
    list_filter = ['status', 'created_at']
    search_fields = [
        'participant__username', 'challenge__title', 
        'team_name'
    ]
    readonly_fields = [
        'started_at', 'submitted_at', 'completed_at',
        'created_at', 'updated_at'
    ]
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('participant', 'challenge', 'challenge__study_group')

@admin.register(MentorshipRelationship, site=custom_admin_site)
class MentorshipRelationshipAdmin(admin.ModelAdmin):
    list_display = [
        'mentor', 'mentee', 'status', 'subject_areas_display',
        'started_at', 'created_at'
    ]
    list_filter = ['status', 'created_at']
    search_fields = ['mentor__username', 'mentee__username', 'goals']
    readonly_fields = ['started_at', 'ended_at', 'created_at', 'updated_at']
    
    def subject_areas_display(self, obj):
        return ', '.join(obj.subject_areas) if obj.subject_areas else '-'
    subject_areas_display.short_description = 'Subject Areas'

@admin.register(MentorshipSession, site=custom_admin_site)
class MentorshipSessionAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'relationship', 'session_type', 'status',
        'scheduled_start', 'actual_start', 'rating', 'created_at'
    ]
    list_filter = ['session_type', 'status', 'rating', 'scheduled_start']
    search_fields = ['title', 'agenda', 'relationship__mentor__username', 'relationship__mentee__username']
    readonly_fields = [
        'actual_start', 'actual_end', 'created_at', 'updated_at'
    ]
    date_hierarchy = 'scheduled_start'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related(
            'relationship', 'relationship__mentor', 'relationship__mentee'
        )