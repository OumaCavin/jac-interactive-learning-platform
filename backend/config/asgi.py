# JAC Platform Configuration - Settings by Cavin Otieno

"""
ASGI Configuration - JAC Learning Platform

ASGI (Asynchronous Server Gateway Interface) configuration for Django,
supporting WebSocket connections and real-time features.

Author: Cavin Otieno
Created: 2025-11-26
"""

import os
from django.core.asgi import get_asgi_application

# Set the default Django settings module for the ASGI application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

django_asgi_app = get_asgi_application()

# Import WebSocket routing
from apps.progress.routing import websocket_urlpatterns
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})