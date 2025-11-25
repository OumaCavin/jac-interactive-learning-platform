"""
Gamification Admin Configuration - JAC Learning Platform

Django admin interface configuration for gamification models.

Author: MiniMax Agent
Created: 2025-11-26
"""

from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count
from .models import (
    Badge, UserBadge, Achievement, UserAchievement,
    UserPoints, PointTransaction, UserLevel, LearningStreak,
    LevelRequirement, AchievementProgress
)


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ['icon', 'name', 'category', 'difficulty', 'rarity', 'is_active', 'created_at']
    list_filter = ['category', 'difficulty', 'rarity', 'is_active']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Badge Information', {
            'fields': ('name', 'description', 'icon')
        }),
        ('Classification', {
            'fields': ('category', 'difficulty', 'rarity')
        }),
        ('Requirements', {
            'fields': ('requirements', 'minimum_points', 'unlock_conditions')
        }),
        ('Settings', {
            'fields': ('is_active',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ['user', 'badge', 'earned_at', 'earned_through', 'is_verified']
    list_filter = ['is_verified', 'badge__category', 'badge__difficulty']
    search_fields = ['user__username', 'badge__name', 'earned_through']
    readonly_fields = ['earned_at', 'verified_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'badge')


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['icon', 'title', 'category', 'difficulty', 'criteria_type', 'points_reward', 'is_active', 'unlock_order']
    list_filter = ['category', 'difficulty', 'criteria_type', 'is_active']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Achievement Information', {
            'fields': ('title', 'description', 'icon')
        }),
        ('Classification', {
            'fields': ('category', 'difficulty')
        }),
        ('Criteria', {
            'fields': ('criteria_type', 'criteria_value', 'criteria_operator')
        }),
        ('Rewards', {
            'fields': ('points_reward', 'badge')
        }),
        ('Settings', {
            'fields': ('is_active', 'unlock_order')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ['user', 'achievement', 'current_progress', 'is_completed', 'completed_at', 'points_earned']
    list_filter = ['is_completed', 'achievement__category', 'achievement__difficulty']
    search_fields = ['user__username', 'achievement__title']
    readonly_fields = ['started_at', 'last_progress_update']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'achievement', 'badge_earned')


@admin.register(UserPoints)
class UserPointsAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_points', 'available_points', 'lifetime_points', 'last_earned', 'last_spent']
    list_filter = ['last_earned', 'last_spent']
    search_fields = ['user__username']
    readonly_fields = ['updated_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')


@admin.register(PointTransaction)
class PointTransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'transaction_type', 'source', 'description', 'balance_after', 'created_at']
    list_filter = ['transaction_type', 'source', 'created_at']
    search_fields = ['user__username', 'source', 'description']
    readonly_fields = ['created_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')


@admin.register(UserLevel)
class UserLevelAdmin(admin.ModelAdmin):
    list_display = ['user', 'current_level', 'current_xp', 'total_xp', 'xp_to_next_level', 'progress_percentage', 'last_level_up']
    list_filter = ['current_level', 'last_level_up']
    search_fields = ['user__username']
    readonly_fields = ['updated_at']
    
    def progress_percentage(self, obj):
        return f"{obj.progress_percentage:.1f}%"
    progress_percentage.short_description = 'Progress %'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')


@admin.register(LearningStreak)
class LearningStreakAdmin(admin.ModelAdmin):
    list_display = ['user', 'current_streak', 'longest_streak', 'streak_multiplier', 'last_activity_date']
    list_filter = ['current_streak', 'longest_streak', 'last_activity_date']
    search_fields = ['user__username']
    readonly_fields = ['created_at', 'updated_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')


@admin.register(LevelRequirement)
class LevelRequirementAdmin(admin.ModelAdmin):
    list_display = ['level', 'requirement_type', 'requirement_value', 'badge', 'title']
    list_filter = ['requirement_type']
    search_fields = ['title', 'description']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('badge')


@admin.register(AchievementProgress)
class AchievementProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'achievement', 'current_count', 'target_count', 'last_update']
    list_filter = ['achievement__category', 'achievement__difficulty', 'last_update']
    search_fields = ['user__username', 'achievement__title']
    readonly_fields = ['last_update']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'achievement')


# Custom admin site configuration
class GamificationAdminSite(admin.AdminSite):
    site_header = "JAC Learning Platform - Gamification"
    site_title = "Gamification Admin"
    index_title = "Gamification Management Dashboard"

gamification_admin_site = GamificationAdminSite(name='gamification_admin')

# Register models with custom admin site
gamification_admin_site.register(Badge, BadgeAdmin)
gamification_admin_site.register(UserBadge, UserBadgeAdmin)
gamification_admin_site.register(Achievement, AchievementAdmin)
gamification_admin_site.register(UserAchievement, UserAchievementAdmin)
gamification_admin_site.register(UserPoints, UserPointsAdmin)
gamification_admin_site.register(PointTransaction, PointTransactionAdmin)
gamification_admin_site.register(UserLevel, UserLevelAdmin)
gamification_admin_site.register(LearningStreak, LearningStreakAdmin)
gamification_admin_site.register(LevelRequirement, LevelRequirementAdmin)
gamification_admin_site.register(AchievementProgress, AchievementProgressAdmin)