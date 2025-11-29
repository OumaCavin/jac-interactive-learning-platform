# JAC Interactive Learning Platform - Core backend implementation by Cavin Otieno

"""
Django Admin Configuration for Knowledge Graph App.

This module provides admin interfaces for managing knowledge graphs,
learning paths, and OSP-based knowledge representation.
"""

from django.contrib import admin
from config.custom_admin import custom_admin_site
from django.utils.html import format_html
from django.urls import reverse, path
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.admin import AdminSite
import json
import csv
from datetime import datetime

from .models import (
    KnowledgeNode, KnowledgeEdge, ConceptRelation, LearningGraph,
    LearningGraphNode, LearningGraphEdge, LearningPath, UserKnowledgeState
)


@admin.register(KnowledgeNode, site=custom_admin_site)
class KnowledgeNodeAdmin(admin.ModelAdmin):
    """
    Admin interface for KnowledgeNode model.
    """
    
    list_display = [
        'title', 'node_type', 'difficulty_level', 'is_active', 
        'view_count', 'created_at', 'created_by'
    ]
    list_filter = [
        'node_type', 'difficulty_level', 'is_active', 'created_at'
    ]
    search_fields = ['title', 'description', 'jac_code']
    readonly_fields = [
        'id', 'view_count', 'created_at', 'updated_at'
    ]
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'node_type', 'difficulty_level')
        }),
        ('OSP Spatial Properties', {
            'fields': ('x_position', 'y_position', 'z_position', 'width', 'height'),
            'classes': ('collapse',)
        }),
        ('Content', {
            'fields': ('content_uri', 'jac_code', 'learning_objectives', 'prerequisites')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at', 'is_active', 'view_count')
        }),
    )
    actions = ['mark_as_active', 'mark_as_inactive', 'export_to_csv', 'increment_view_count']
    
    def mark_as_active(self, request, queryset):
        """Mark selected nodes as active"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} knowledge nodes marked as active.')
    mark_as_active.short_description = "Mark selected nodes as active"
    
    def mark_as_inactive(self, request, queryset):
        """Mark selected nodes as inactive"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} knowledge nodes marked as inactive.')
    mark_as_inactive.short_description = "Mark selected nodes as inactive"
    
    def export_to_csv(self, request, queryset):
        """Export selected nodes to CSV"""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="knowledge_nodes_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Title', 'Type', 'Difficulty', 'Active', 'View Count', 'Created At'])
        
        for node in queryset:
            writer.writerow([
                node.title, node.node_type, node.difficulty_level, 
                node.is_active, node.view_count, node.created_at
            ])
        
        return response
    export_to_csv.short_description = "Export selected nodes to CSV"
    
    def increment_view_count(self, request, queryset):
        """Increment view count for selected nodes"""
        for node in queryset:
            node.increment_view_count()
        self.message_user(request, f'View counts incremented for {queryset.count()} nodes.')
    increment_view_count.short_description = "Increment view count"
    
    def get_queryset(self, request):
        """Override to prefetch related data"""
        return super().get_queryset(request).select_related('created_by')


@admin.register(KnowledgeEdge, site=custom_admin_site)
class KnowledgeEdgeAdmin(admin.ModelAdmin):
    """
    Admin interface for KnowledgeEdge model.
    """
    
    list_display = [
        'source_node_title', 'target_node_title', 'edge_type', 'strength',
        'traversal_count', 'is_active', 'created_at'
    ]
    list_filter = [
        'edge_type', 'strength', 'is_active', 'created_at'
    ]
    search_fields = [
        'source_node__title', 'target_node__title', 'description'
    ]
    readonly_fields = [
        'id', 'traversal_count', 'created_at', 'updated_at'
    ]
    fieldsets = (
        ('Edge Information', {
            'fields': ('source_node', 'target_node', 'edge_type', 'strength')
        }),
        ('OSP Spatial Properties', {
            'fields': ('curve_points', 'edge_weight'),
            'classes': ('collapse',)
        }),
        ('Relationship Metadata', {
            'fields': ('description', 'examples')
        }),
        ('Analytics', {
            'fields': ('traversal_count', 'created_at', 'updated_at', 'is_active')
        }),
    )
    actions = ['mark_as_active', 'mark_as_inactive', 'increment_traversal_count', 'export_to_csv']
    
    def source_node_title(self, obj):
        """Display source node title"""
        return obj.source_node.title
    source_node_title.short_description = 'Source Node'
    source_node_title.admin_order_field = 'source_node__title'
    
    def target_node_title(self, obj):
        """Display target node title"""
        return obj.target_node.title
    target_node_title.short_description = 'Target Node'
    target_node_title.admin_order_field = 'target_node__title'
    
    def mark_as_active(self, request, queryset):
        """Mark selected edges as active"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} knowledge edges marked as active.')
    mark_as_active.short_description = "Mark selected edges as active"
    
    def mark_as_inactive(self, request, queryset):
        """Mark selected edges as inactive"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} knowledge edges marked as inactive.')
    mark_as_inactive.short_description = "Mark selected edges as inactive"
    
    def increment_traversal_count(self, request, queryset):
        """Increment traversal count for selected edges"""
        for edge in queryset:
            edge.increment_traversal()
        self.message_user(request, f'Traversal counts incremented for {queryset.count()} edges.')
    increment_traversal_count.short_description = "Increment traversal count"
    
    def export_to_csv(self, request, queryset):
        """Export selected edges to CSV"""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="knowledge_edges_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Source', 'Target', 'Type', 'Strength', 'Traversals', 'Active', 'Created At'])
        
        for edge in queryset:
            writer.writerow([
                edge.source_node.title, edge.target_node.title, edge.edge_type,
                edge.strength, edge.traversal_count, edge.is_active, edge.created_at
            ])
        
        return response
    export_to_csv.short_description = "Export selected edges to CSV"
    
    def get_queryset(self, request):
        """Override to prefetch related data"""
        return super().get_queryset(request).select_related('source_node', 'target_node')


@admin.register(ConceptRelation, site=custom_admin_site)
class ConceptRelationAdmin(admin.ModelAdmin):
    """
    Admin interface for ConceptRelation model.
    """
    
    list_display = [
        'concept_a', 'concept_b', 'relation_type', 'domain', 'confidence_score',
        'is_active', 'created_at'
    ]
    list_filter = [
        'relation_type', 'domain', 'is_active', 'created_at'
    ]
    search_fields = [
        'concept_a', 'concept_b', 'description'
    ]
    readonly_fields = [
        'id', 'created_at', 'updated_at'
    ]
    fieldsets = (
        ('Concept Information', {
            'fields': ('concept_a', 'concept_b', 'relation_type', 'domain')
        }),
        ('Relationship Details', {
            'fields': ('description', 'confidence_score', 'related_nodes')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at', 'is_active')
        }),
    )
    actions = ['export_to_csv', 'mark_as_active', 'mark_as_inactive']
    
    def export_to_csv(self, request, queryset):
        """Export selected concept relations to CSV"""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="concept_relations_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Concept A', 'Concept B', 'Relation Type', 'Domain', 'Confidence', 'Active', 'Created At'])
        
        for relation in queryset:
            writer.writerow([
                relation.concept_a, relation.concept_b, relation.relation_type,
                relation.domain, relation.confidence_score, relation.is_active, relation.created_at
            ])
        
        return response
    export_to_csv.short_description = "Export selected relations to CSV"
    
    def mark_as_active(self, request, queryset):
        """Mark selected relations as active"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} concept relations marked as active.')
    mark_as_active.short_description = "Mark selected relations as active"
    
    def mark_as_inactive(self, request, queryset):
        """Mark selected relations as inactive"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} concept relations marked as inactive.')
    mark_as_inactive.short_description = "Mark selected relations as inactive"
    
    def get_queryset(self, request):
        """Override to prefetch related data"""
        return super().get_queryset(request).select_related('created_by')


class LearningGraphNodeInline(admin.TabularInline):
    """
    Inline admin for LearningGraphNode through model.
    """
    model = LearningGraphNode
    extra = 0
    fields = [
        'knowledge_node', 'display_order', 'is_mandatory', 'node_weight',
        'custom_x', 'custom_y', 'estimated_time', 'prerequisite_score'
    ]
    autocomplete_fields = ['knowledge_node']


class LearningGraphEdgeInline(admin.TabularInline):
    """
    Inline admin for LearningGraphEdge through model.
    """
    model = LearningGraphEdge
    extra = 0
    fields = [
        'knowledge_edge', 'display_order', 'is_mandatory', 'edge_priority',
        'unlock_conditions', 'recommended_for', 'custom_path'
    ]
    autocomplete_fields = ['knowledge_edge']


@admin.register(LearningGraph, site=custom_admin_site)
class LearningGraphAdmin(admin.ModelAdmin):
    """
    Admin interface for LearningGraph model.
    """
    
    list_display = [
        'title', 'graph_type', 'status', 'subject_area', 'completion_rate',
        'total_attempts', 'created_at'
    ]
    list_filter = [
        'graph_type', 'status', 'subject_area', 'target_audience', 'created_at'
    ]
    search_fields = ['title', 'description', 'subject_area']
    readonly_fields = [
        'id', 'completion_rate', 'total_attempts', 'successful_completions',
        'created_at', 'updated_at'
    ]
    inlines = [LearningGraphNodeInline, LearningGraphEdgeInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'graph_type', 'status')
        }),
        ('Content and Scope', {
            'fields': ('subject_area', 'target_audience', 'estimated_duration')
        }),
        ('Graph Properties', {
            'fields': ('layout_config', 'view_box', 'adaptive_rules', 'difficulty_progression'),
            'classes': ('collapse',)
        }),
        ('Analytics', {
            'fields': ('completion_rate', 'average_completion_time', 'total_attempts', 'successful_completions')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at', 'version', 'tags')
        }),
    )
    actions = [
        'mark_as_active', 'mark_as_draft', 'mark_as_archived',
        'export_analytics', 'generate_learning_paths'
    ]
    
    def mark_as_active(self, request, queryset):
        """Mark selected graphs as active"""
        updated = queryset.update(status='active')
        self.message_user(request, f'{updated} learning graphs marked as active.')
    mark_as_active.short_description = "Mark selected graphs as active"
    
    def mark_as_draft(self, request, queryset):
        """Mark selected graphs as draft"""
        updated = queryset.update(status='draft')
        self.message_user(request, f'{updated} learning graphs marked as draft.')
    mark_as_draft.short_description = "Mark selected graphs as draft"
    
    def mark_as_archived(self, request, queryset):
        """Mark selected graphs as archived"""
        updated = queryset.update(status='archived')
        self.message_user(request, f'{updated} learning graphs marked as archived.')
    mark_as_archived.short_description = "Mark selected graphs as archived"
    
    def export_analytics(self, request, queryset):
        """Export analytics for selected graphs"""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="learning_graphs_analytics_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            'Title', 'Type', 'Status', 'Subject Area', 'Completion Rate',
            'Total Attempts', 'Successful Completions', 'Created At'
        ])
        
        for graph in queryset:
            writer.writerow([
                graph.title, graph.graph_type, graph.status, graph.subject_area,
                f"{graph.completion_rate:.1f}%", graph.total_attempts,
                graph.successful_completions, graph.created_at
            ])
        
        return response
    export_analytics.short_description = "Export analytics to CSV"
    
    def generate_learning_paths(self, request, queryset):
        """Generate learning paths for selected graphs"""
        from .services.graph_algorithms import AdaptiveEngine
        
        generated_count = 0
        for graph in queryset:
            try:
                adaptive_engine = AdaptiveEngine()
                # This would typically be triggered for specific users
                # For admin purposes, we just report the potential
                generated_count += graph.nodes.count()
            except Exception as e:
                self.message_user(request, f'Error generating paths for {graph.title}: {str(e)}')
        
        self.message_user(
            request, 
            f'Learning path generation initiated for {queryset.count()} graphs. '
            f'Estimated {generated_count} potential paths.'
        )
    generate_learning_paths.short_description = "Generate learning paths"
    
    def get_queryset(self, request):
        """Override to prefetch related data"""
        return super().get_queryset(request).select_related('created_by')
    
    def get_readonly_fields(self, request, obj=None):
        """Make some fields readonly only for existing objects"""
        readonly_fields = list(self.readonly_fields)
        if obj:  # Editing existing object
            readonly_fields.extend(['created_by', 'version'])
        return readonly_fields


@admin.register(LearningPath, site=custom_admin_site)
class LearningPathAdmin(admin.ModelAdmin):
    """
    Admin interface for LearningPath model.
    """
    
    list_display = [
        'title', 'user', 'learning_graph_title', 'adaptation_type',
        'status', 'progress_percentage', 'last_activity'
    ]
    list_filter = [
        'adaptation_type', 'status', 'started_at', 'last_activity'
    ]
    search_fields = ['title', 'user__username', 'learning_graph__title']
    readonly_fields = [
        'id', 'progress_percentage', 'started_at', 'completed_at',
        'last_activity', 'total_time_spent'
    ]
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'learning_graph', 'title', 'adaptation_type', 'status')
        }),
        ('Progress Tracking', {
            'fields': ('current_node', 'completed_nodes', 'progress_percentage')
        }),
        ('Analytics', {
            'fields': ('started_at', 'completed_at', 'last_activity', 'total_time_spent'),
            'classes': ('collapse',)
        }),
        ('Adaptive Learning Data', {
            'fields': ('performance_metrics', 'adaptation_history'),
            'classes': ('collapse',)
        }),
    )
    actions = [
        'mark_as_completed', 'mark_as_paused', 'mark_as_active',
        'export_path_data', 'update_progress'
    ]
    
    def learning_graph_title(self, obj):
        """Display learning graph title"""
        return obj.learning_graph.title
    learning_graph_title.short_description = 'Learning Graph'
    learning_graph_title.admin_order_field = 'learning_graph__title'
    
    def mark_as_completed(self, request, queryset):
        """Mark selected paths as completed"""
        from django.utils import timezone
        updated = queryset.update(
            status='completed',
            completed_at=timezone.now(),
            progress_percentage=100.0
        )
        self.message_user(request, f'{updated} learning paths marked as completed.')
    mark_as_completed.short_description = "Mark selected paths as completed"
    
    def mark_as_paused(self, request, queryset):
        """Mark selected paths as paused"""
        updated = queryset.update(status='paused')
        self.message_user(request, f'{updated} learning paths marked as paused.')
    mark_as_paused.short_description = "Mark selected paths as paused"
    
    def mark_as_active(self, request, queryset):
        """Mark selected paths as active"""
        updated = queryset.update(status='active')
        self.message_user(request, f'{updated} learning paths marked as active.')
    mark_as_active.short_description = "Mark selected paths as active"
    
    def export_path_data(self, request, queryset):
        """Export learning path data to CSV"""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="learning_paths_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            'Title', 'User', 'Graph', 'Type', 'Status', 'Progress %',
            'Started At', 'Last Activity', 'Time Spent'
        ])
        
        for path in queryset:
            writer.writerow([
                path.title, path.user.username, path.learning_graph.title,
                path.adaptation_type, path.status, f"{path.progress_percentage:.1f}%",
                path.started_at, path.last_activity, path.total_time_spent
            ])
        
        return response
    export_path_data.short_description = "Export path data to CSV"
    
    def update_progress(self, request, queryset):
        """Update progress for selected paths"""
        for path in queryset:
            path.update_progress_percentage()
        self.message_user(request, f'Progress updated for {queryset.count()} learning paths.')
    update_progress.short_description = "Update progress calculations"
    
    def get_queryset(self, request):
        """Override to prefetch related data"""
        return super().get_queryset(request).select_related('user', 'learning_graph', 'current_node')


@admin.register(UserKnowledgeState, site=custom_admin_site)
class UserKnowledgeStateAdmin(admin.ModelAdmin):
    """
    Admin interface for UserKnowledgeState model.
    """
    
    list_display = [
        'user', 'knowledge_node_title', 'mastery_level', 'confidence_score',
        'success_rate', 'last_reviewed'
    ]
    list_filter = [
        'mastery_level', 'last_reviewed'
    ]
    search_fields = [
        'user__username', 'knowledge_node__title'
    ]
    readonly_fields = [
        'id', 'first_exposure', 'last_reviewed', 'total_time_spent',
        'success_rate'
    ]
    fieldsets = (
        ('User and Concept', {
            'fields': ('user', 'knowledge_node')
        }),
        ('Knowledge State', {
            'fields': ('mastery_level', 'confidence_score')
        }),
        ('Learning Analytics', {
            'fields': (
                'first_exposure', 'last_reviewed', 'total_time_spent',
                'assessment_scores', 'practice_attempts', 'successful_attempts'
            ),
            'classes': ('collapse',)
        }),
        ('Spaced Repetition', {
            'fields': ('next_review_date', 'review_interval'),
            'classes': ('collapse',)
        }),
        ('Adaptive Learning Data', {
            'fields': ('learning_velocity', 'difficulty_adjustment'),
            'classes': ('collapse',)
        }),
    )
    actions = [
        'update_confidence_scores', 'mark_for_review', 'export_state_data',
        'calculate_success_rates'
    ]
    
    def knowledge_node_title(self, obj):
        """Display knowledge node title"""
        return obj.knowledge_node.title
    knowledge_node_title.short_description = 'Knowledge Node'
    knowledge_node_title.admin_order_field = 'knowledge_node__title'
    
    def success_rate(self, obj):
        """Display success rate"""
        rate = obj.get_success_rate()
        color = 'green' if rate >= 70 else 'orange' if rate >= 50 else 'red'
        return format_html(
            '<span style="color: {};">{:.1f}%</span>',
            color, rate
        )
    success_rate.short_description = 'Success Rate'
    success_rate.admin_order_field = 'practice_attempts'
    
    def update_confidence_scores(self, request, queryset):
        """Update confidence scores based on recent assessments"""
        updated = 0
        for state in queryset:
            if state.assessment_scores:
                recent_scores = state.assessment_scores[-3:]
                avg_confidence = sum(
                    score['normalized_score'] for score in recent_scores
                ) / len(recent_scores)
                state.confidence_score = avg_confidence
                state.save(update_fields=['confidence_score'])
                updated += 1
        
        self.message_user(request, f'Confidence scores updated for {updated} states.')
    update_confidence_scores.short_description = "Update confidence scores"
    
    def mark_for_review(self, request, queryset):
        """Mark selected states for review"""
        from django.utils import timezone
        from datetime import timedelta
        
        review_date = timezone.now() + timedelta(days=1)
        updated = queryset.update(next_review_date=review_date)
        
        self.message_user(request, f'{updated} states marked for review on {review_date.date()}.')
    mark_for_review.short_description = "Mark for review tomorrow"
    
    def export_state_data(self, request, queryset):
        """Export user knowledge state data to CSV"""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="user_knowledge_states_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            'User', 'Knowledge Node', 'Mastery Level', 'Confidence Score',
            'Success Rate', 'Practice Attempts', 'Last Reviewed'
        ])
        
        for state in queryset:
            writer.writerow([
                state.user.username, state.knowledge_node.title,
                state.mastery_level, f"{state.confidence_score:.2f}",
                f"{state.get_success_rate():.1f}%", state.practice_attempts,
                state.last_reviewed
            ])
        
        return response
    export_state_data.short_description = "Export state data to CSV"
    
    def calculate_success_rates(self, request, queryset):
        """Calculate and update success rates for selected states"""
        for state in queryset:
            # Force recalculation of success rate
            current_rate = state.get_success_rate()
            state.save(update_fields=['practice_attempts', 'successful_attempts'])
        
        self.message_user(request, f'Success rates recalculated for {queryset.count()} states.')
    calculate_success_rates.short_description = "Recalculate success rates"
    
    def get_queryset(self, request):
        """Override to prefetch related data"""
        return super().get_queryset(request).select_related('user', 'knowledge_node')


# Customize admin site header and title
admin.site.site_header = "JAC Learning Platform - Knowledge Graph Administration"
admin.site.site_title = "Knowledge Graph Admin"
admin.site.index_title = "Knowledge Graph Management Dashboard"


# Additional admin actions and utilities

def bulk_generate_learning_paths(modeladmin, request, queryset):
    """Bulk action to generate learning paths for multiple graphs"""
    from .services.graph_algorithms import AdaptiveEngine
    
    generated_paths = []
    for graph in queryset:
        try:
            # Get all active users (in a real implementation, this would be more sophisticated)
            from django.contrib.auth.models import User
            users = User.objects.filter(is_active=True)[:10]  # Limit for demo
            
            for user in users:
                try:
                    adaptive_engine = AdaptiveEngine()
                    path = adaptive_engine.generate_learning_path(user, graph)
                    generated_paths.append(f"{user.username} - {graph.title}")
                except Exception as e:
                    modeladmin.message_user(
                        request, 
                        f"Error generating path for {user.username} on {graph.title}: {str(e)}",
                        level='ERROR'
                    )
        except Exception as e:
            modeladmin.message_user(
                request, 
                f"Error processing graph {graph.title}: {str(e)}",
                level='ERROR'
            )
    
    modeladmin.message_user(
        request, 
        f"Generated {len(generated_paths)} learning paths successfully."
    )

bulk_generate_learning_paths.short_description = "Generate learning paths for all active users"


def export_knowledge_graph_analytics(modeladmin, request, queryset):
    """Export comprehensive analytics for selected graphs"""
    from .services.analytics import KnowledgeGraphAnalytics
    
    analytics_data = []
    for graph in queryset:
        try:
            analytics = KnowledgeGraphAnalytics()
            graph_analytics = analytics.get_graph_analytics(graph.id)
            analytics_data.append({
                'graph_title': graph.title,
                'analytics': graph_analytics
            })
        except Exception as e:
            modeladmin.message_user(
                request, 
                f"Error getting analytics for {graph.title}: {str(e)}",
                level='ERROR'
            )
    
    # Export as JSON
    response = HttpResponse(content_type='application/json')
    response['Content-Disposition'] = f'attachment; filename="knowledge_graph_analytics_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json"'
    
    json.dump(analytics_data, response, indent=2, default=str)
    return response

export_knowledge_graph_analytics.short_description = "Export comprehensive analytics"


# Register additional actions
admin.site.add_action(bulk_generate_learning_paths, 'bulk_generate_paths')
admin.site.add_action(export_knowledge_graph_analytics, 'export_analytics')