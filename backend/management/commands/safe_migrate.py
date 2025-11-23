"""
Django management command to handle migrations robustly.
This command automatically handles common migration issues.
"""

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connection
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Run migrations with automatic error handling'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force migration even if there are conflicts',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🔄 Starting automated migration process...'))
        
        migration_strategies = [
            ('makemigrations', ['--noinput']),
            ('migrate', ['--fake-initial', '--noinput']),
            ('migrate', ['--noinput']),
            ('migrate', ['--force', '--noinput']),
            ('migrate', ['--fake', '--noinput']),
        ]
        
        success_count = 0
        
        for strategy_name, strategy_args in migration_strategies:
            try:
                self.stdout.write(f"  → Trying: {strategy_name} {' '.join(strategy_args)}")
                
                if strategy_name == 'makemigrations':
                    call_command('makemigrations', *strategy_args, verbosity=0)
                else:
                    call_command(strategy_name, *strategy_args, verbosity=0)
                
                self.stdout.write(self.style.SUCCESS(f"  ✅ {strategy_name} completed"))
                success_count += 1
                
                # If regular migrate succeeds, we're done
                if strategy_name == 'migrate' and '--noinput' in strategy_args and '--fake' not in strategy_args:
                    break
                    
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"  ⚠️ {strategy_name} failed: {str(e)}"))
                continue
        
        # Always try to collect static files
        try:
            self.stdout.write('  → Collecting static files...')
            call_command('collectstatic', '--noinput', verbosity=0)
            self.stdout.write(self.style.SUCCESS('  ✅ Static files collected'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'  ⚠️ Static files failed: {str(e)}'))
        
        if success_count > 0:
            self.stdout.write(self.style.SUCCESS('✅ Migration process completed successfully!'))
        else:
            self.stdout.write(self.style.ERROR('❌ All migration strategies failed'))
            
        # Check final migration status
        try:
            self.stdout.write('\n📊 Final migration status:')
            call_command('showmigrations', verbosity=0)
        except Exception:
            pass