"""
Content URL configuration
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'content', views.ContentViewSet, basename='content')
router.register(r'recommendations', views.ContentRecommendationViewSet, basename='contentrecommendation')

urlpatterns = [
    path('', include(router.urls)),
]
