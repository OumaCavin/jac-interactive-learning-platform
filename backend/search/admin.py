"""
Admin configuration for search app
"""

from django.contrib import admin
from .models import SearchQuery, SearchResult
from config.custom_admin import custom_admin_site


@admin.register(SearchQuery, site=custom_admin_site)
class SearchQueryAdmin(admin.ModelAdmin):
    list_display = ['query', 'user', 'results_count', 'created_at']
    list_filter = ['created_at', 'user']
    search_fields = ['query']
    readonly_fields = ['created_at']
    
    def has_change_permission(self, request, obj=None):
        return False  # Search queries should not be edited


@admin.register(SearchResult, site=custom_admin_site)
class SearchResultAdmin(admin.ModelAdmin):
    list_display = ['title', 'content_type', 'relevance_score', 'popularity_score', 'created_at']
    list_filter = ['content_type', 'created_at']
    search_fields = ['title', 'description', 'query']
    readonly_fields = ['created_at', 'updated_at']