"""
Mock JWT Authentication for Development
This middleware allows mock tokens from frontend to pass through Django authentication
"""

import jwt
from django.conf import settings
from rest_framework import authentication, exceptions


class MockJWTAuthentication(authentication.BaseAuthentication):
    """
    Mock JWT Authentication that accepts frontend mock tokens
    For development only - allows tokens like 'mock-jwt-token-{timestamp}'
    """
    
    def authenticate(self, request):
        """
        Authenticate using mock JWT tokens
        """
        auth_header = request.headers.get('Authorization', '')
        
        if not auth_header.startswith('Bearer '):
            return None
            
        token = auth_header.split(' ')[1]
        
        # Check if this is a mock token
        if token.startswith('mock-jwt-token-') or token.startswith('mock-admin-jwt-token-'):
            # Create a mock user based on token type
            if 'admin' in token:
                # Admin user
                user = type('MockUser', (), {
                    'id': '2',
                    'username': 'admin_user',
                    'email': 'admin@jac.com',
                    'is_staff': True,
                    'is_superuser': True,
                    'is_authenticated': True,
                    'is_anonymous': False,
                    'is_active': True,
                })()
            else:
                # Regular user
                user = type('MockUser', (), {
                    'id': '1',
                    'username': 'demo_user',
                    'email': 'demo@example.com',
                    'is_staff': False,
                    'is_superuser': False,
                    'is_authenticated': True,
                    'is_anonymous': False,
                    'is_active': True,
                })()
            
            return (user, token)
        
        # For real JWT tokens, try standard JWT authentication
        if settings.ENVIRONMENT == 'production':
            try:
                from rest_framework_simplejwt.backends import TokenBackend
                token_backend = TokenBackend(
                    algorithm='HS256',
                    signing_key=settings.SECRET_KEY,
                    verify=True
                )
                valid_token = token_backend.decode(token, verify=True)
                
                # Create user from token payload
                user_data = valid_token
                user_id = user_data.get('user_id')
                
                if user_id:
                    from apps.users.models import User
                    try:
                        user = User.objects.get(id=user_id)
                        return (user, token)
                    except User.DoesNotExist:
                        pass
                        
            except Exception as e:
                pass
        
        return None

    def authenticate_header(self, request):
        """
        Return a string to be used as the value of the `WWW-Authenticate`
        header in a `401 Unauthenticated` response, or `None` if the
        authentication scheme should return `403 Permission Denied` responses.
        """
        return 'Bearer'