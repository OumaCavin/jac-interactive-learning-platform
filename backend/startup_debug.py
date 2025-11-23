#!/usr/bin/env python3
"""
Debug script to help diagnose backend startup issues
"""

import os
import sys
import django
import time
from datetime import datetime

def debug_backend_startup():
    """Debug backend startup process"""
    print(f"[DEBUG] Starting backend debug at {datetime.now()}")
    
    # Set Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    
    try:
        print("[DEBUG] Setting up Django...")
        django.setup()
        print("[DEBUG] Django setup completed successfully")
        
        # Test database connection
        print("[DEBUG] Testing database connection...")
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        print("[DEBUG] Database connection successful")
        
        # Test basic imports
        print("[DEBUG] Testing basic imports...")
        from django.contrib.auth.models import User
        from apps.users.models import UserProfile
        from apps.learning.models import LearningPath
        print("[DEBUG] All imports successful")
        
        # Test health endpoint manually
        print("[DEBUG] Testing health endpoint...")
        from django.http import JsonResponse
        from django.test import RequestFactory
        from apps.agents.views import system_health_check
        
        factory = RequestFactory()
        request = factory.get('/api/health/')
        response = system_health_check(request)
        
        print(f"[DEBUG] Health endpoint response: {response.content}")
        print("[DEBUG] All tests passed!")
        
        return True
        
    except Exception as e:
        print(f"[DEBUG] ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = debug_backend_startup()
    sys.exit(0 if success else 1)