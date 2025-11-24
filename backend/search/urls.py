"""
URL configuration for search app
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create router for ViewSets
router = DefaultRouter()
router.register(r'search', views.SearchViewSet, basename='search')
router.register(r'history', views.SearchHistoryViewSet, basename='search-history')
router.register(r'popular', views.PopularSearchesViewSet, basename='popular-searches')

urlpatterns = [
    path('', include(router.urls)),
]