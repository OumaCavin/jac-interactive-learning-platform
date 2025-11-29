"""
Custom createsuperuser command for JAC Platform custom User model.
This ensures superuser permissions are properly set.
"""

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from apps.users.models import User


class Command(BaseCommand):
    help = 'Create a superuser for the JAC Platform with proper permissions'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            dest='username',
            default=None,
            help='Specifies the username for the superuser.',
        )
        parser.add_argument(
            '--email',
            dest='email',
            default=None,
            help='Specifies the email for the superuser.',
        )
        parser.add_argument(
            '--noinput',
            action='store_false',
            dest='interactive',
            default=True,
            help='Tells Django to NOT prompt the user for input of any kind. '
                 'You must use --username and --email with --noinput.',
        )
        parser.add_argument(
            '--password',
            dest='password',
            default=None,
            help='Specifies the password for the superuser.',
        )

    def handle(self, *args, **options):
        username = options.get('username')
        email = options.get('email')
        interactive = options.get('interactive')
        password = options.get('password')

        # Get the custom User model
        User = get_user_model()

        # Validate inputs
        if not username:
            if interactive:
                username = self._get_input_string(self.stdout.write, 'Username: ')
            else:
                raise CommandError('--username is required with --noinput')

        if not email:
            if interactive:
                email = self._get_input_string(self.stdout.write, 'Email: ')
            else:
                raise CommandError('--email is required with --noinput')

        if not password:
            if interactive:
                password = self._get_input_password()
            else:
                raise CommandError('--password is required with --noinput')

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            raise CommandError('A user with that username already exists.')

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            raise CommandError('A user with that email already exists.')

        # Validate password
        try:
            validate_password(password)
        except ValidationError as e:
            raise CommandError('Password validation failed: ' + '; '.join(e.messages))

        # Create the superuser with proper permissions
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            
            # Explicitly set superuser permissions
            user.is_superuser = True
            user.is_staff = True
            user.is_active = True
            user.save()
            
            self.stdout.write(
                self.style.SUCCESS(f'Superuser "{username}" created successfully with admin permissions!')
            )
            self.stdout.write(
                self.style.SUCCESS(f'Username: {username}')
            )
            self.stdout.write(
                self.style.SUCCESS(f'Email: {email}')
            )
            self.stdout.write(
                self.style.SUCCESS(f'Superuser: {user.is_superuser}')
            )
            self.stdout.write(
                self.style.SUCCESS(f'Staff: {user.is_staff}')
            )
            self.stdout.write(
                self.style.SUCCESS(f'Active: {user.is_active}')
            )
            
        except Exception as e:
            raise CommandError(f'Error creating superuser: {e}')

    def _get_input_string(self, stdout, message):
        """Helper method to get string input from user."""
        raw_value = input(message)
        return raw_value.strip()

    def _get_input_password(self):
        """Helper method to get password input with confirmation."""
        password = ''
        password2 = ''
        while password != password2:
            password = input('Password: ')
            password2 = input('Password (again): ')
            if password != password2:
                stdout = self.stdout
                stdout.write(self.style.ERROR('Passwords do not match. Please try again.'))
                stdout.write('')
            else:
                break
        return password