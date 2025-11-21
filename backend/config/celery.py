"""
Celery configuration for the JAC Learning Platform backend.
"""

import os
from celery import Celery

# Set the default Django settings module for the 'celery' program
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Create the Celery instance
celery_app = Celery('config')

# Load task modules from all registered Django app configs
celery_app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks from all installed apps
celery_app.autodiscover_tasks()

# Celery task routing and settings
celery_app.conf.update(
    # Task routing
    task_routes={
        'apps.learning.tasks.*': {'queue': 'learning'},
        'apps.users.tasks.*': {'queue': 'users'},
        'apps.content.tasks.*': {'queue': 'content'},
    },
    
    # Task execution settings
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    
    # Task result backend settings
    result_expires=3600,
    task_ignore_result=False,
    
    # Worker settings
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
    
    # Beat scheduler settings
    beat_scheduler='django_celery_beat.schedulers:DatabaseScheduler',
    
    # Task retry settings
    task_acks_late=True,
    worker_send_task_events=True,
    task_send_sent_event=True,
)

# Task definitions for background processing
@celery_app.task(bind=True)
def debug_task(self):
    """Debug task for testing Celery configuration"""
    print(f'Request: {self.request!r}')
    return "Celery is working!"

# Example task for content processing
@celery_app.task(bind=True, name='content.process_content')
def process_content_task(self, content_id):
    """Example background task for content processing"""
    print(f'Processing content ID: {content_id}')
    # Add actual content processing logic here
    return f"Content {content_id} processed successfully"

# Example task for user operations
@celery_app.task(bind=True, name='users.send_welcome_email')
def send_welcome_email_task(self, user_id):
    """Example background task for user email notifications"""
    print(f'Sending welcome email to user: {user_id}')
    # Add actual email sending logic here
    return f"Welcome email sent to user {user_id}"