# JAC Interactive Learning Platform - Core backend implementation by Cavin Otieno

"""
Django management command to initialize the JAC Learning Platform.
Automatically runs migrations, creates superuser, and sets up initial data.
"""

import os
import sys
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from django.db import connection
from django.conf import settings
from django.utils import timezone


class Command(BaseCommand):
    """Initialize the JAC Learning Platform with migrations and superuser."""

    help = 'Initialize the JAC Learning Platform: run migrations and create superuser'

    def add_arguments(self, parser):
        """Add command line arguments."""
        parser.add_argument(
            '--no-superuser',
            action='store_true',
            help='Skip superuser creation',
        )
        parser.add_argument(
            '--username',
            type=str,
            default='admin',
            help='Superuser username (default: admin)',
        )
        parser.add_argument(
            '--email',
            type=str,
            default='admin@platform.local',
            help='Superuser email (default: admin@platform.local)',
        )
        parser.add_argument(
            '--password',
            type=str,
            help='Superuser password (REQUIRED for production)',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force initialization even if tables exist',
        )

    def handle(self, *args, **options):
        """Handle the command execution."""
        self.stdout.write(
            self.style.SUCCESS('🚀 Starting JAC Learning Platform initialization...')
        )

        # Check if database connection works
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                self.stdout.write(
                    self.style.SUCCESS('✅ Database connection successful')
                )
        except Exception as e:
            raise CommandError(f'❌ Database connection failed: {e}')

        # Run migrations
        self.run_migrations()

        # Create superuser if not skipped and password is provided
        if not options['no_superuser']:
            if not options['password']:
                raise CommandError('Password is required for superuser creation. Use --password option.')
            
            self.create_superuser(
                username=options['username'],
                email=options['email'],
                password=options['password']
            )

        # Show completion message
        self.stdout.write(
            self.style.SUCCESS('🎉 JAC Learning Platform initialization completed!')
        )
        self.stdout.write(
            self.style.SUCCESS(f'Admin URL: http://localhost:8000/admin/')
        )
        self.stdout.write(
            self.style.SUCCESS(f'API URL: http://localhost:8000/api/')
        )

    def run_migrations(self):
        """Run database migrations."""
        self.stdout.write('📦 Running database migrations...')
        
        from django.core.management import call_command
        
        try:
            # Run makemigrations first to check for new models
            self.stdout.write('  • Checking for new model changes...')
            call_command('makemigrations', interactive=False, verbosity=1)
            
            # Run migrate
            self.stdout.write('  • Applying migrations...')
            call_command('migrate', interactive=False, verbosity=1)
            
            # Collect static files if in production
            if not settings.DEBUG:
                self.stdout.write('  • Collecting static files...')
                call_command('collectstatic', interactive=False, verbosity=1)
            
            self.stdout.write(
                self.style.SUCCESS('✅ Migrations completed successfully')
            )
            
        except Exception as e:
            raise CommandError(f'❌ Migration failed: {e}')

    def create_superuser(self, username, email, password):
        """Create superuser account."""
        User = get_user_model()
        
        self.stdout.write(f'👤 Creating superuser: {username}')
        
        try:
            # Check if superuser already exists
            if User.objects.filter(username=username).exists():
                self.stdout.write(
                    self.style.WARNING(f'⚠️  Superuser "{username}" already exists')
                )
                return

            # Create superuser
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
                first_name='Admin',
                last_name='User'
            )

            # Set additional profile fields
            user.learning_style = 'visual'
            user.preferred_difficulty = 'beginner'
            user.learning_pace = 'moderate'
            user.agent_interaction_level = 'high'
            user.email_notifications = True
            user.save()

            self.stdout.write(
                self.style.SUCCESS(f'✅ Superuser created: {username}')
            )
            self.stdout.write(
                self.style.SUCCESS(f'   Email: {email}')
            )
            self.stdout.write(
                self.style.SUCCESS(f'   Password: {password}')
            )

        except Exception as e:
            raise CommandError(f'❌ Superuser creation failed: {e}')


# Also create the management module structure
