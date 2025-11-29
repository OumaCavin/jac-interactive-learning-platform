#!/usr/bin/env python
"""
Session and Authentication Debug Script
Check session configuration and authentication flow
"""
import sys
import os

sys.path.insert(0, '/workspace/jac-interactive-learning-platform/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

def debug_session_auth():
    """Debug session and authentication configuration"""
    from django.conf import settings
    from django.contrib.auth import get_user_model
    from django.contrib.sessions.models import Session
    from config.custom_admin import custom_admin_site
    
    print("🔍 Session & Authentication Debug")
    print("=" * 40)
    
    # Check session settings
    print("\n📝 Session Configuration:")
    print(f"   SESSION_ENGINE: {settings.SESSION_ENGINE}")
    print(f"   SESSION_COOKIE_AGE: {settings.SESSION_COOKIE_AGE}")
    print(f"   SESSION_COOKIE_NAME: {settings.SESSION_COOKIE_NAME}")
    print(f"   SESSION_COOKIE_SAMESITE: {getattr(settings, 'SESSION_COOKIE_SAMESITE', 'Not set')}")
    
    # Check authentication settings
    print("\n🔐 Authentication Settings:")
    print(f"   AUTHENTICATION_BACKENDS: {settings.AUTHENTICATION_BACKENDS}")
    print(f"   LOGIN_URL: {settings.LOGIN_URL}")
    print(f"   LOGIN_REDIRECT_URL: {settings.LOGIN_REDIRECT_URL}")
    print(f"   LOGOUT_REDIRECT_URL: {getattr(settings, 'LOGOUT_REDIRECT_URL', 'Not set')}")
    
    # Check admin middleware
    print("\n⚙️  Middleware (Admin relevant):")
    middleware = settings.MIDDLEWARE
    auth_middleware = [m for m in middleware if 'auth' in m.lower()]
    session_middleware = [m for m in middleware if 'session' in m.lower()]
    print(f"   Auth middleware: {auth_middleware}")
    print(f"   Session middleware: {session_middleware}")
    
    # Check user authentication
    User = get_user_model()
    try:
        user = User.objects.get(username='Ouma')
        print(f"\n👤 User Authentication Status:")
        print(f"   Username: {user.username}")
        print(f"   Has password: {bool(user.has_usable_password())}")
        print(f"   Is authenticated: User is loaded from DB")
        
        # Check if user can authenticate
        from django.contrib.auth import authenticate
        auth_user = authenticate(username='Ouma', password='your_password_here')
        if auth_user:
            print(f"   ✅ Authentication successful")
        else:
            print(f"   ❌ Authentication failed (check password)")
            
    except User.DoesNotExist:
        print("\n❌ User 'Ouma' not found!")
    
    # Check active sessions (development)
    print(f"\n🗂️  Active Sessions:")
    session_count = Session.objects.count()
    print(f"   Total sessions: {session_count}")
    
    print(f"\n💡 Troubleshooting Steps:")
    print(f"   1. Try logging out completely and logging back in")
    print(f"   2. Clear browser cookies for localhost:8000")
    print(f"   3. Try incognito/private browser mode")
    print(f"   4. Check if CSRF token issues in browser console")
    
    print(f"\n🎯 Admin URLs to test:")
    print(f"   http://localhost:8000/admin/ (custom admin)")
    print(f"   http://localhost:8000/admin/login/ (login page)")

if __name__ == "__main__":
    debug_session_auth()