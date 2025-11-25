"""
WebSocket URL Routing - JAC Learning Platform

WebSocket routing configuration for real-time dashboard feeds,
live alerts, and continuous performance monitoring.

URL Patterns:
- /ws/dashboard/ - Real-time dashboard updates
- /ws/alerts/ - Alert and notification stream
- /ws/metrics/ - Real-time performance metrics
- /ws/activity/ - Live activity stream

Author: MiniMax Agent
Created: 2025-11-26
"""

from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/predictive/$', consumers.PredictiveAnalyticsConsumer.as_asgi()),
    re_path(r'ws/ai-interaction/$', consumers.AIInteractionConsumer.as_asgi()),
    re_path(r'ws/dashboard/$', consumers.DashboardConsumer.as_asgi()),
    re_path(r'ws/alerts/$', consumers.AlertConsumer.as_asgi()),
    re_path(r'ws/metrics/$', consumers.RealtimeMetricsConsumer.as_asgi()),
    re_path(r'ws/activity/$', consumers.ActivityStreamConsumer.as_asgi()),
]