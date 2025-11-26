# JAC Interactive Learning Platform - Core backend implementation by Cavin Otieno

"""
Admin interface configuration for JAC Code Execution

This module defines the Django admin interface configuration for
managing code executions, templates, and security settings.
"""

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib import messages
from .models import CodeExecution, ExecutionTemplate, CodeExecutionSession, SecuritySettings


@admin.register(CodeExecution)
class CodeExecutionAdmin(admin.ModelAdmin):
    """Admin interface for code execution records."""
    
    list_display = [
        'id', 'user', 'language', 'status', 'return_code', 
        'execution_time', 'created_at', 'view_details'
    ]
    list_filter = ['language', 'status', 'created_at']
    search_fields = ['user__username', 'code', 'stdout', 'stderr']
    readonly_fields = [
        'id', 'execution_time', 'memory_usage', 'completed_at',
        'created_at', 'stdout', 'stderr', 'output'
    ]
    ordering = ['-created_at']
    
    fieldsets = (
        ('Execution Details', {
            'fields': ('id', 'user', 'language', 'code', 'stdin')
        }),
        ('Results', {
            'fields': ('status', 'stdout', 'stderr', 'output', 'return_code')
        }),
        ('Performance', {
            'fields': ('execution_time', 'memory_usage', 'max_execution_time', 'max_memory', 'max_output_size')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'completed_at')
        }),
    )
    
    def view_details(self, obj):
        """Link to view execution details."""
        url = reverse('admin:jac_execution_codeexecution_change', args=[obj.id])
        return format_html('<a href="{}">View Details</a>', url)
    view_details.short_description = 'Actions'
    
    def has_change_permission(self, request, obj=None):
        """Allow changing execution status."""
        return True
    
    def has_add_permission(self, request):
        """Allow adding execution records."""
        return True


@admin.register(ExecutionTemplate)
class ExecutionTemplateAdmin(admin.ModelAdmin):
    """Admin interface for execution templates."""
    
    list_display = [
        'name', 'language', 'category', 'created_by', 
        'is_public', 'is_active', 'created_at', 'updated_at'
    ]
    list_filter = ['language', 'is_public', 'is_active', 'category', 'created_at']
    search_fields = ['name', 'description', 'code', 'created_by__username']
    readonly_fields = ['created_at', 'updated_at', 'id']
    ordering = ['-updated_at']
    
    fieldsets = (
        ('Template Information', {
            'fields': ('id', 'name', 'description', 'language', 'category', 'tags')
        }),
        ('Code Content', {
            'fields': ('code', 'stdin')
        }),
        ('Access Control', {
            'fields': ('is_public', 'is_active')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """Set created_by field when creating new templates."""
        if not change:  # If creating a new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(CodeExecutionSession)
class CodeExecutionSessionAdmin(admin.ModelAdmin):
    """Admin interface for execution sessions."""
    
    list_display = [
        'session_id', 'user', 'total_executions', 'success_rate',
        'total_execution_time', 'started_at', 'is_active'
    ]
    list_filter = ['is_active', 'started_at']
    search_fields = ['session_id', 'user__username']
    readonly_fields = [
        'id', 'success_rate', 'total_executions', 'successful_executions',
        'failed_executions', 'total_execution_time', 'started_at', 'last_activity'
    ]
    ordering = ['-started_at']
    
    def success_rate(self, obj):
        """Display success rate as percentage."""
        return f"{obj.success_rate:.1f}%"
    success_rate.short_description = 'Success Rate'


@admin.register(SecuritySettings)
class SecuritySettingsAdmin(admin.ModelAdmin):
    """Admin interface for security settings."""
    
    list_display = ['id', 'max_execution_time', 'max_memory', 'max_code_size', 'updated_at']
    readonly_fields = ['created_at', 'updated_at', 'id']
    
    fieldsets = (
        ('Resource Limits', {
            'fields': ('max_execution_time', 'max_memory', 'max_output_size', 'max_code_size')
        }),
        ('Language Settings', {
            'fields': ('allowed_languages',)
        }),
        ('Security Options', {
            'fields': ('enable_sandboxing', 'enable_network_access', 'blocked_imports', 'blocked_functions')
        }),
        ('Rate Limiting', {
            'fields': ('max_executions_per_minute', 'max_executions_per_hour')
        }),
        ('Metadata', {
            'fields': ('id', 'created_at', 'updated_at')
        }),
    )
    
    def has_add_permission(self, request):
        """Allow adding only if no settings exist."""
        return not SecuritySettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of security settings."""
        return False


# Custom admin actions
@admin.action(description='Mark executions as reviewed')
def mark_as_reviewed(modeladmin, request, queryset):
    """Custom action to mark executions as reviewed."""
    queryset.update(status='reviewed')
    messages.success(request, f'{queryset.count()} executions marked as reviewed.')


@admin.action(description='Export execution data to JSON')
def export_execution_data(modeladmin, request, queryset):
    """Custom action to export execution data."""
    import json
    from django.http import HttpResponse
    
    data = []
    for execution in queryset:
        data.append({
            'id': str(execution.id),
            'user': execution.user.username,
            'language': execution.language,
            'status': execution.status,
            'execution_time': execution.execution_time,
            'created_at': execution.created_at.isoformat(),
        })
    
    response = HttpResponse(
        json.dumps(data, indent=2),
        content_type='application/json'
    )
    response['Content-Disposition'] = 'attachment; filename=execution_data.json'
    return response


# Add custom actions to CodeExecutionAdmin
CodeExecutionAdmin.actions = [mark_as_reviewed, export_execution_data]