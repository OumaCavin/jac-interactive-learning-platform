"""
Search service for JAC Learning Platform
Handles search functionality across all content types
"""

import re
from typing import List, Dict, Any, Optional
from django.db.models import Q
from django.contrib.auth import get_user_model
from collections import defaultdict

from ..models import SearchQuery, SearchResult

User = get_user_model()


class SearchService:
    """
    Main search service that handles searches across all content types
    """
    
    def __init__(self):
        self.content_types = {
            'learning_path': self._search_learning_paths,
            'module': self._search_modules,
            'lesson': self._search_lessons,
            'assessment': self._search_assessments,
            'knowledge_node': self._search_knowledge_nodes,
            'content': self._search_content,
            'user': self._search_users,
        }
    
    def search(self, query: str, user: Optional[User] = None, content_types: Optional[List[str]] = None, 
               limit: int = 20, offset: int = 0) -> Dict[str, Any]:
        """
        Perform a comprehensive search across all content types
        
        Args:
            query: Search query string
            user: Current user (optional)
            content_types: List of content types to search in (optional)
            limit: Maximum number of results
            offset: Number of results to skip
            
        Returns:
            Dictionary with search results and metadata
        """
        if not query.strip():
            return {
                'query': query,
                'results': [],
                'total_results': 0,
                'suggestions': [],
                'facets': {}
            }
        
        # Track search query
        search_query = self._track_search_query(query, user)
        
        # Determine which content types to search
        if content_types is None:
            content_types = list(self.content_types.keys())
        
        # Perform searches across content types
        all_results = []
        facet_counts = defaultdict(int)
        
        for content_type in content_types:
            if content_type in self.content_types:
                try:
                    results = self.content_types[content_type](query, user)
                    all_results.extend(results)
                    
                    # Count results for facets
                    facet_counts[content_type] = len(results)
                except Exception as e:
                    print(f"Error searching {content_type}: {e}")
        
        # Sort results by relevance score
        all_results.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        # Apply pagination
        paginated_results = all_results[offset:offset + limit]
        
        # Get search suggestions
        suggestions = self._get_search_suggestions(query)
        
        # Create facets
        facets = {
            'content_types': dict(facet_counts),
            'total_results': len(all_results)
        }
        
        # Update search query with results count
        if search_query:
            search_query.results_count = len(all_results)
            search_query.save()
        
        return {
            'query': query,
            'results': paginated_results,
            'total_results': len(all_results),
            'suggestions': suggestions,
            'facets': facets
        }
    
    def get_suggestions(self, query: str, limit: int = 10) -> List[str]:
        """
        Get search suggestions for autocomplete
        
        Args:
            query: Partial search query
            limit: Maximum number of suggestions
            
        Returns:
            List of suggested search terms
        """
        if len(query) < 2:
            return []
        
        # Get popular search queries that start with the query
        suggestions = []
        
        # Query database for similar searches
        similar_queries = SearchQuery.objects.filter(
            query__istartswith=query
        ).values_list('query', flat=True).distinct()[:limit]
        
        suggestions.extend(similar_queries)
        
        # Get suggestions from content titles
        content_suggestions = self._get_content_suggestions(query, limit)
        suggestions.extend(content_suggestions)
        
        # Remove duplicates and limit results
        suggestions = list(dict.fromkeys(suggestions))[:limit]
        
        return suggestions
    
    def _search_learning_paths(self, query: str, user: Optional[User] = None) -> List[Dict[str, Any]]:
        """Search learning paths"""
        from apps.learning.models import LearningPath
        
        search_terms = query.lower().split()
        q_objects = Q()
        
        for term in search_terms:
            q_objects |= Q(title__icontains=term)
            q_objects |= Q(description__icontains=term)
            q_objects |= Q(objectives__icontains=term)
        
        learning_paths = LearningPath.objects.filter(q_objects, is_published=True)
        
        results = []
        for lp in learning_paths[:50]:  # Limit results
            # Calculate relevance score
            relevance = self._calculate_relevance(query, lp.title, lp.description)
            
            results.append({
                'content_type': 'learning_path',
                'content_id': str(lp.id),
                'title': lp.title,
                'description': lp.description[:200] + '...' if len(lp.description) > 200 else lp.description,
                'url': f'/learning/paths/{lp.id}',
                'tags': lp.tags if hasattr(lp, 'tags') else [],
                'relevance_score': relevance,
                'popularity_score': 0.8 if lp.is_featured else 0.5,
                'metadata': {
                    'difficulty': lp.difficulty_level,
                    'estimated_hours': lp.estimated_hours,
                    'prerequisites': lp.prerequisites if hasattr(lp, 'prerequisites') else []
                }
            })
        
        return results
    
    def _search_modules(self, query: str, user: Optional[User] = None) -> List[Dict[str, Any]]:
        """Search modules"""
        from apps.learning.models import Module
        
        search_terms = query.lower().split()
        q_objects = Q()
        
        for term in search_terms:
            q_objects |= Q(title__icontains=term)
            q_objects |= Q(description__icontains=term)
            q_objects |= Q(learning_objectives__icontains=term)
        
        modules = Module.objects.filter(q_objects, is_published=True)
        
        results = []
        for module in modules[:50]:
            relevance = self._calculate_relevance(query, module.title, module.description)
            
            results.append({
                'content_type': 'module',
                'content_id': str(module.id),
                'title': module.title,
                'description': module.description[:200] + '...' if len(module.description) > 200 else module.description,
                'url': f'/learning/modules/{module.id}',
                'tags': [],
                'relevance_score': relevance,
                'popularity_score': 0.7,
                'metadata': {
                    'difficulty': module.difficulty_level,
                    'estimated_hours': module.estimated_duration,
                    'lesson_count': module.lessons.count() if hasattr(module, 'lessons') else 0
                }
            })
        
        return results
    
    def _search_lessons(self, query: str, user: Optional[User] = None) -> List[Dict[str, Any]]:
        """Search lessons"""
        from apps.learning.models import Lesson
        
        search_terms = query.lower().split()
        q_objects = Q()
        
        for term in search_terms:
            q_objects |= Q(title__icontains=term)
            q_objects |= Q(content__icontains=term)
            q_objects |= Q(learning_objectives__icontains=term)
        
        lessons = Lesson.objects.filter(q_objects, is_published=True)
        
        results = []
        for lesson in lessons[:50]:
            relevance = self._calculate_relevance(query, lesson.title, lesson.content[:100])
            
            results.append({
                'content_type': 'lesson',
                'content_id': str(lesson.id),
                'title': lesson.title,
                'description': lesson.content[:200] + '...' if len(lesson.content) > 200 else lesson.content,
                'url': f'/learning/lessons/{lesson.id}',
                'tags': [],
                'relevance_score': relevance,
                'popularity_score': 0.6,
                'metadata': {
                    'type': lesson.lesson_type,
                    'duration': lesson.duration_minutes
                }
            })
        
        return results
    
    def _search_assessments(self, query: str, user: Optional[User] = None) -> List[Dict[str, Any]]:
        """Search assessments"""
        from apps.assessments.models import Assessment
        
        search_terms = query.lower().split()
        q_objects = Q()
        
        for term in search_terms:
            q_objects |= Q(title__icontains=term)
            q_objects |= Q(description__icontains=term)
        
        assessments = Assessment.objects.filter(q_objects, is_published=True)
        
        results = []
        for assessment in assessments[:50]:
            relevance = self._calculate_relevance(query, assessment.title, assessment.description)
            
            results.append({
                'content_type': 'assessment',
                'content_id': str(assessment.id),
                'title': assessment.title,
                'description': assessment.description[:200] + '...' if len(assessment.description) > 200 else assessment.description,
                'url': f'/assessments/{assessment.id}',
                'tags': [],
                'relevance_score': relevance,
                'popularity_score': 0.7,
                'metadata': {
                    'type': assessment.assessment_type,
                    'difficulty': assessment.difficulty_level,
                    'time_limit': assessment.time_limit,
                    'max_attempts': assessment.max_attempts
                }
            })
        
        return results
    
    def _search_knowledge_nodes(self, query: str, user: Optional[User] = None) -> List[Dict[str, Any]]:
        """Search knowledge graph nodes"""
        from apps.knowledge_graph.models import KnowledgeNode
        
        search_terms = query.lower().split()
        q_objects = Q()
        
        for term in search_terms:
            q_objects |= Q(title__icontains=term)
            q_objects |= Q(description__icontains=term)
            q_objects |= Q(content__icontains=term)
        
        nodes = KnowledgeNode.objects.filter(q_objects)
        
        results = []
        for node in nodes[:50]:
            relevance = self._calculate_relevance(query, node.title, node.description or node.content)
            
            results.append({
                'content_type': 'knowledge_node',
                'content_id': str(node.id),
                'title': node.title,
                'description': (node.description or node.content)[:200] + '...' if len(node.description or node.content) > 200 else (node.description or node.content),
                'url': f'/knowledge-graph/node/{node.id}',
                'tags': [],
                'relevance_score': relevance,
                'popularity_score': 0.5,
                'metadata': {
                    'node_type': node.node_type,
                    'difficulty': node.difficulty_level,
                    'connections_count': node.connections.count() if hasattr(node, 'connections') else 0
                }
            })
        
        return results
    
    def _search_content(self, query: str, user: Optional[User] = None) -> List[Dict[str, Any]]:
        """Search general content"""
        from apps.content.models import Content
        
        search_terms = query.lower().split()
        q_objects = Q()
        
        for term in search_terms:
            q_objects |= Q(title__icontains=term)
            q_objects |= Q(body__icontains=term)
        
        content_items = Content.objects.filter(q_objects, is_published=True)
        
        results = []
        for content in content_items[:50]:
            relevance = self._calculate_relevance(query, content.title, content.body[:100])
            
            results.append({
                'content_type': 'content',
                'content_id': str(content.id),
                'title': content.title,
                'description': content.body[:200] + '...' if len(content.body) > 200 else content.body,
                'url': f'/content/{content.id}',
                'tags': content.tags if hasattr(content, 'tags') else [],
                'relevance_score': relevance,
                'popularity_score': 0.5,
                'metadata': {
                    'content_type': content.content_type,
                    'author': str(content.author) if hasattr(content, 'author') else None
                }
            })
        
        return results
    
    def _search_users(self, query: str, user: Optional[User] = None) -> List[Dict[str, Any]]:
        """Search users"""
        search_terms = query.lower().split()
        q_objects = Q()
        
        for term in search_terms:
            q_objects |= Q(username__icontains=term)
            q_objects |= Q(first_name__icontains=term)
            q_objects |= Q(last_name__icontains=term)
            q_objects |= Q(email__icontains=term)
        
        users = User.objects.filter(q_objects, is_active=True)
        
        results = []
        for u in users[:20]:  # Limit user results
            relevance = self._calculate_relevance(query, u.username, f"{u.first_name} {u.last_name}")
            
            results.append({
                'content_type': 'user',
                'content_id': str(u.id),
                'title': f"{u.first_name} {u.last_name}" if u.first_name and u.last_name else u.username,
                'description': f"@{u.username} - {u.email}",
                'url': f'/profile/{u.username}',
                'tags': ['user'],
                'relevance_score': relevance,
                'popularity_score': 0.3,
                'metadata': {
                    'username': u.username,
                    'email': u.email,
                    'is_staff': u.is_staff,
                    'is_instructor': getattr(u, 'is_instructor', False)
                }
            })
        
        return results
    
    def _calculate_relevance(self, query: str, title: str, content: str) -> float:
        """
        Calculate relevance score based on query term frequency in title and content
        """
        query_terms = query.lower().split()
        title_lower = title.lower()
        content_lower = (content or "").lower()
        
        score = 0.0
        
        # Title matches are weighted higher
        for term in query_terms:
            if term in title_lower:
                score += 0.7
            if term in content_lower:
                score += 0.3
        
        # Normalize by number of terms
        if query_terms:
            score = min(score / len(query_terms), 1.0)
        
        return score
    
    def _track_search_query(self, query: str, user: Optional[User] = None) -> Optional[SearchQuery]:
        """Track search query for analytics and suggestions"""
        try:
            search_query = SearchQuery.objects.create(
                query=query,
                user=user,
                results_count=0
            )
            return search_query
        except Exception:
            return None
    
    def _get_search_suggestions(self, query: str, limit: int = 5) -> List[str]:
        """Get search suggestions based on popular queries"""
        suggestions = []
        
        try:
            # Get similar searches from search history
            similar_queries = SearchQuery.objects.filter(
                query__icontains=query
            ).values_list('query', flat=True).distinct()[:limit]
            
            suggestions.extend(similar_queries)
        except Exception:
            pass
        
        return suggestions[:limit]
    
    def _get_content_suggestions(self, query: str, limit: int = 5) -> List[str]:
        """Get content-based search suggestions"""
        suggestions = []
        
        try:
            # Get popular learning path titles
            from apps.learning.models import LearningPath
            lp_titles = LearningPath.objects.filter(
                title__icontains=query
            ).values_list('title', flat=True)[:limit//2]
            suggestions.extend(lp_titles)
            
            # Get popular module titles
            from apps.learning.models import Module
            module_titles = Module.objects.filter(
                title__icontains=query
            ).values_list('title', flat=True)[:limit//2]
            suggestions.extend(module_titles)
            
        except Exception:
            pass
        
        return suggestions[:limit]