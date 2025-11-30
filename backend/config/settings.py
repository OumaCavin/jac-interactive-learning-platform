# JAC Platform Configuration - Settings by Cavin Otieno

"""
Django settings for the JAC Learning Platform backend.
"""

import os
from pathlib import Path
from decouple import config

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Sentry Error Monitoring - Import and initialize
try:
    from .sentry import init_sentry_monitoring
    init_sentry_monitoring()
except ImportError:
    # Sentry is optional - continue without it if not available
    pass

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-development-key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=lambda v: [s.strip() for s in v.split(',')])

# Application definition
DJANGO_APPS = [
    'django.contrib.admin',  # Re-enabled - custom admin configuration active
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'mptt',  # Re-enabled for tree structures
    'django_celery_beat',  # Re-enabled for task scheduling
    'drf_spectacular',     # Re-enabled for API documentation
    'django_extensions',   # Re-enabled for Django extensions
    'channels',  # Re-enabled for WebSocket support
]

LOCAL_APPS = [
    'apps.users',
    'apps.learning',
    'apps.content',
    'apps.assessments',
    'apps.progress',  # Re-enabled
    'apps.agents',
    'apps.knowledge_graph',  # Re-enabled
    'apps.jac_execution',  # Re-enabled
    'apps.gamification',
    'apps.collaboration',  # Re-enabled
    'apps.management',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'

# Database
# Database Configuration - PostgreSQL for production/Docker
# SQLite commented out for PostgreSQL setup
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# Database Configuration - Using PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='jac_learning_db'),
        'USER': config('DB_USER', default='jac_user'),
        'PASSWORD': config('DB_PASSWORD', default='jac_password'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
        'TEST': {
            'NAME': 'test_jac_learning_db',
        },
    }
}

# Caching - Using Redis for production
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': config('REDIS_URL', default='redis://redis:6379/1'),
    }
}

# Session Storage - Using database for sessions
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 86400  # 24 hours

# Celery Configuration - Re-enabled for production
CELERY_BROKER_URL = config('CELERY_BROKER_URL', default='redis://redis:6379/0')
CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND', default='redis://redis:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
CELERY_WORKER_CONCURRENCY = 4
CELERY_WORKER_MAX_TASKS_PER_CHILD = 1000

# Jaseci Configuration
JASECCI_URL = config('JASECCI_URL', default='http://localhost:8001')
JASECCI_API_KEY = config('JASECCI_API_KEY', default='')

# Gemini AI Configuration
GEMINI_API_KEY = config('GEMINI_API_KEY', default='AIzaSyDxeppnc1cpepvU9OwV0QZ-mUTk-zfeZEM')

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Custom User Model
AUTH_USER_MODEL = 'users.User'

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
# Use a writable location for static root to avoid permission issues
STATIC_ROOT = '/var/www/static'  # Docker volume mount path (same as nginx)
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# For development, serve static files from both STATIC_ROOT and STATICFILES_DIRS
if DEBUG:
    # In development, serve from both local static files and the collected STATIC_ROOT
    STATICFILES_DIRS = [
        BASE_DIR / 'static',
        '/var/www/static',  # Add the Docker volume mount path
    ]
else:
    # For production, use STATIC_ROOT (already set above)
    pass

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Django REST Framework Configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',  # Re-enabled - drf_spectacular installed
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour',
        'jac_execution': '50/hour',
    }
}

# Development Environment Auth Configuration
if config('ENVIRONMENT', default='development') == 'development':
    # For development, allow mock tokens and make some endpoints public
    REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] = (
        'apps.learning.middleware.MockJWTAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    )
    
    # Allow public access to learning paths for development
    REST_FRAMEWORK['DEFAULT_PERMISSION_CLASSES'] = (
        'rest_framework.permissions.AllowAny',
    )
else:
    # Production: Strict authentication
    REST_FRAMEWORK['DEFAULT_PERMISSION_CLASSES'] = (
        'rest_framework.permissions.IsAuthenticated',
    )

# JWT Configuration
from datetime import timedelta
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

# CORS Configuration
CORS_ALLOW_ALL_ORIGINS = config('CORS_ALLOW_ALL_ORIGINS', default=True, cast=bool)
CORS_ALLOWED_ORIGINS = config(
    'CORS_ALLOWED_ORIGINS', 
    default='http://localhost:3000,http://127.0.0.1:3000',
    cast=lambda v: [s.strip() for s in v.split(',')]
)

# Logging Configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'apps': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# Spectacular OpenAPI Configuration - Re-enabled
SPECTACULAR_SETTINGS = {
    'TITLE': 'JAC Learning Platform API',
    'DESCRIPTION': 'API for the JAC Interactive Learning Platform with multi-agent system',
    'VERSION': '1.0.0',
}

# Email Configuration
EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = config('EMAIL_HOST', default='localhost')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@jacplatform.com')
EMAIL_TIMEOUT = config('EMAIL_TIMEOUT', default=30, cast=int)

# Knowledge Graph Configuration
KNOWLEDGE_GRAPH_CONFIG = {
    'MAX_NODES_PER_GRAPH': 1000,
    'MAX_EDGES_PER_GRAPH': 5000,
    'CACHE_TIMEOUT': 3600,  # 1 hour
}

# JAC Execution Configuration
JAC_EXECUTION_CONFIG = {
    'MAX_CODE_SIZE': 10240,  # 10KB
    'MAX_EXECUTION_TIME': 30,  # seconds
    'MAX_MEMORY_USAGE': 128,  # MB
    'SANDBOX_ENABLED': True,
}

# Agent Configuration
AGENT_CONFIG = {
    'CONTENT_CURATOR': {
        'cache_timeout': 1800,  # 30 minutes
        'max_content_items': 100,
    },
    'QUIZ_MASTER': {
        'cache_timeout': 900,   # 15 minutes
        'max_questions_per_quiz': 20,
    },
    'EVALUATOR': {
        'cache_timeout': 600,   # 10 minutes
        'code_analysis_depth': 'deep',
    },
    'PROGRESS_TRACKER': {
        'cache_timeout': 300,   # 5 minutes
        'metrics_retention_days': 365,
    },
    'MOTIVATOR': {
        'cache_timeout': 1800,  # 30 minutes
        'gamification_enabled': True,
    },
    'ORCHESTRATOR': {
        'cache_timeout': 60,    # 1 minute
        'coordination_timeout': 10,
    }
}

# Custom Error Handlers for Admin
def custom_403_handler(request, exception):
    """Custom 403 error handler that uses admin templates."""
    from django.template.response import TemplateResponse
    from django.contrib import admin
    
    # Return custom 403 template
    return TemplateResponse(
        request=request,
        template='admin/403.html',
        context={'user': request.user},
        status=403,
        using=None
    )

def custom_404_handler(request, exception):
    """Custom 404 error handler."""
    from django.template.response import TemplateResponse
    
    return TemplateResponse(
        request=request,
        template='admin/404.html',
        context={'request': request},
        status=404,
        using=None
    )

def custom_500_handler(request):
    """Custom 500 error handler."""
    from django.template.response import TemplateResponse
    
    return TemplateResponse(
        request=request,
        template='admin/500.html',
        context={'request': request},
        status=500,
        using=None
    )

# Register custom error handlers
handler403 = 'config.settings.custom_403_handler'
handler404 = 'config.settings.custom_404_handler'
handler500 = 'config.settings.custom_500_handler'