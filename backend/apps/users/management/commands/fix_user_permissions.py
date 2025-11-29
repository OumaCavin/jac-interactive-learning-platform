"""
Management command to fix user admin permissions for JAC Platform.
This can be used to fix users created before the custom createsuperuser command.
"""

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from apps.users.models import User


class Command(BaseCommand):
    help = 'Fix admin permissions for existing users'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            dest='username',
            help='Username of the user to fix permissions for',
        )
        parser.add_argument(
            '--all',
            action='store_true',
            dest='fix_all',
            help='Fix permissions for ALL users',
        )
        parser.add_argument(
            '--make-superuser',
            action='store_true',
            dest='make_superuser',
            help='Make the specified user a superuser',
        )

    def handle(self, *args, **options):
        username = options.get('username')
        fix_all = options.get('fix_all')
        make_superuser = options.get('make_superuser')
        
        User = get_user_model()

        if fix_all:
            self.stdout.write('Fixing permissions for ALL users...')
            fixed_count = 0
            for user in User.objects.all():
                self.stdout.write(f'Processing user: {user.username}')
                self._fix_user_permissions(user, make_superuser or user.is_superuser)
                fixed_count += 1
            self.stdout.write(
                self.style.SUCCESS(f'Successfully fixed permissions for {fixed_count} users')
            )
        elif username:
            try:
                user = User.objects.get(username=username)
                self.stdout.write(f'Fixing permissions for user: {user.username}')
                self._fix_user_permissions(user, make_superuser)
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully fixed permissions for user "{username}"')
                )
            except User.DoesNotExist:
                raise CommandError(f'User "{username}" does not exist')
        else:
            raise CommandError('You must specify either --username or --all')

    def _fix_user_permissions(self, user, make_superuser=False):
        """Fix user permissions for JAC Platform custom User model."""
        # Check current permissions
        self.stdout.write(f'  Current - is_superuser: {user.is_superuser}')
        self.stdout.write(f'  Current - is_staff: {user.is_staff}')
        self.stdout.write(f'  Current - is_active: {user.is_active}')

        # Fix permissions
        if make_superuser or user.is_superuser:
            user.is_superuser = True
            user.is_staff = True
            user.is_active = True
            user.save()
            
            self.stdout.write(f'  Fixed - is_superuser: {user.is_superuser}')
            self.stdout.write(f'  Fixed - is_staff: {user.is_staff}')
            self.stdout.write(f'  Fixed - is_active: {user.is_active}')
            self.stdout.write(self.style.SUCCESS('  ✅ Admin permissions applied!'))
        else:
            self.stdout.write('  ℹ️ User is not a superuser, no changes needed.')