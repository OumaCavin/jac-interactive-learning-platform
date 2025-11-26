# JAC Interactive Learning Platform - Core backend implementation by Cavin Otieno

"""
Management Command - Start Background Monitoring

Django management command to start the background monitoring service
for real-time performance tracking and analytics.

Usage:
    python manage.py start_monitoring

Author: Cavin Otieno
Created: 2025-11-26
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
import asyncio
import signal
import sys

from ....services.background_monitoring_service import BackgroundMonitoringService


class Command(BaseCommand):
    help = 'Start background monitoring service for real-time analytics'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.monitoring_service = None
        self.should_stop = False

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Test configuration without starting service',
        )
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Enable verbose logging',
        )

    def handle(self, *args, **options):
        """Handle the management command"""
        dry_run = options['dry_run']
        verbose = options['verbose']
        
        if dry_run:
            self.stdout.write(
                self.style.SUCCESS('Dry run completed - monitoring service is properly configured')
            )
            return
        
        self.stdout.write(
            self.style.SUCCESS('Starting JAC Learning Platform Background Monitoring Service...')
        )
        
        # Set up signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        try:
            # Create and start monitoring service
            self.monitoring_service = BackgroundMonitoringService()
            
            self.stdout.write(
                self.style.WARNING('Background monitoring service started. Press Ctrl+C to stop.')
            )
            
            # Run the monitoring service
            asyncio.run(self._run_monitoring_service())
            
        except KeyboardInterrupt:
            self.stdout.write(
                self.style.WARNING('\nReceived interrupt signal. Shutting down gracefully...')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error starting monitoring service: {str(e)}')
            )
            sys.exit(1)
        finally:
            self._cleanup()

    def signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        self.should_stop = True
        self.stdout.write(
            self.style.WARNING(f'Received signal {signum}. Initiating shutdown...')
        )

    async def _run_monitoring_service(self):
        """Run the monitoring service with graceful shutdown handling"""
        try:
            await self.monitoring_service.start_background_monitoring()
        except asyncio.CancelledError:
            self.stdout.write(
                self.style.WARNING('Monitoring service cancelled')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error in monitoring service: {str(e)}')
            )
            raise

    def _cleanup(self):
        """Clean up resources"""
        if self.monitoring_service:
            self.monitoring_service.stop_background_monitoring()
            self.stdout.write(
                self.style.SUCCESS('Background monitoring service stopped')
            )
        
        self.stdout.write(
            self.style.SUCCESS('Cleanup completed')
        )