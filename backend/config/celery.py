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

# Email verification task
@celery_app.task(bind=True, name='users.send_email_verification')
def send_email_verification_task(self, user_id, verification_url):
    """Send email verification to user"""
    from django.contrib.auth import get_user_model
    from django.core.mail import send_mail
    from django.template.loader import render_to_string
    from django.utils.html import strip_tags
    from django.conf import settings
    
    User = get_user_model()
    try:
        user = User.objects.get(id=user_id)
        
        # Prepare email content
        subject = 'Verify Your JAC Learning Platform Account'
        context = {
            'user': user,
            'verification_url': verification_url,
            'platform_name': 'JAC Learning Platform',
        }
        
        # Render HTML email template
        html_message = render_to_string('emails/verification_email.html', context)
        plain_message = strip_tags(html_message)
        
        # Send email
        send_mail(
            subject=subject,
            message=plain_message,
            html_message=html_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
        
        print(f'✅ Email verification sent successfully to: {user.email}')
        return f"Verification email sent to {user.email}"
        
    except User.DoesNotExist:
        print(f'❌ User with ID {user_id} not found')
        raise self.retry(countdown=60, max_retries=3)
    except Exception as e:
        print(f'❌ Failed to send verification email: {str(e)}')
        raise self.retry(countdown=300, max_retries=2)