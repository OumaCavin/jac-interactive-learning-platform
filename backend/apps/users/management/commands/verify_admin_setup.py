"""
Management command to verify and fix Django admin setup for custom User model.
"""

from django.core.management.base import BaseCommand, CommandError
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.apps import apps
from config.custom_admin import custom_admin_site


class Command(BaseCommand):
    help = 'Verify and fix Django admin setup for the JAC Platform'

    def handle(self, *args, **options):
        self.stdout.write('🔧 Verifying Django admin setup...')
        self.stdout.write('=' * 60)
        
        # Check if custom admin site is being used
        self.stdout.write(f'✅ Custom admin site: {custom_admin_site}')
        self.stdout.write(f'✅ Admin site name: {custom_admin_site.name}')
        
        # Check User model registration
        User = get_user_model()
        self.stdout.write(f'✅ User model: {User.__name__}')
        
        # Check if User is registered with custom admin site
        try:
            user_admin = custom_admin_site._registry.get(User)
            if user_admin:
                self.stdout.write('✅ User model registered with custom admin site')
                self.stdout.write(f'   Admin class: {user_admin.__class__.__name__}')
            else:
                self.stdout.write('❌ User model NOT registered with custom admin site')
                self.stdout.write('   This is the likely cause of the access denied error!')
                
                # Fix: Register User with custom admin site
                from apps.users.admin import UserAdmin
                custom_admin_site.register(User, UserAdmin)
                self.stdout.write('🔧 Registered User model with custom admin site')
                
        except Exception as e:
            self.stdout.write(f'❌ Error checking User registration: {e}')
        
        # Check all app admin registrations
        self.stdout.write('\n📋 Checking all app admin registrations...')
        
        apps_config = apps.get_app_configs()
        registered_models = []
        unregistered_models = []
        
        for app_config in apps_config:
            if app_config.label.startswith('apps.') or app_config.label == 'search':
                self.stdout.write(f'\n📦 App: {app_config.label}')
                
                try:
                    admin_models = list(custom_admin_site._registry.keys())
                    for model in app_config.get_models():
                        if model in admin_models:
                            registered_models.append(f"{app_config.label}.{model.__name__}")
                            self.stdout.write(f'  ✅ {model.__name__}')
                        else:
                            unregistered_models.append(f"{app_config.label}.{model.__name__}")
                            self.stdout.write(f'  ❌ {model.__name__} (not registered)')
                except Exception as e:
                    self.stdout.write(f'  ⚠️ Error checking models: {e}')
        
        self.stdout.write('\n📊 Summary:')
        self.stdout.write(f'  ✅ Registered models: {len(registered_models)}')
        self.stdout.write(f'  ❌ Unregistered models: {len(unregistered_models)}')
        
        if unregistered_models:
            self.stdout.write('\n🔧 Attempting to auto-register unregistered models...')
            self._auto_register_models()
        
        # Check current user permissions
        self.stdout.write('\n👤 Checking user permissions...')
        for user in User.objects.all():
            self.stdout.write(f'  User: {user.username}')
            self.stdout.write(f'    is_superuser: {user.is_superuser}')
            self.stdout.write(f'    is_staff: {user.is_staff}')
            self.stdout.write(f'    is_active: {user.is_active}')
        
        self.stdout.write('\n🎉 Admin verification completed!')
        self.stdout.write('\n💡 If you were getting "Access Denied", the User model should now be properly registered.')

    def _auto_register_models(self):
        """Auto-register models that aren't registered yet"""
        from django.contrib.admin import site as default_site
        
        apps_config = apps.get_app_configs()
        registered_with_custom = set(custom_admin_site._registry.keys())
        
        for app_config in apps_config:
            if app_config.label.startswith('apps.') or app_config.label == 'search':
                for model in app_config.get_models():
                    if model not in registered_with_custom:
                        try:
                            # Try to get admin from default site
                            default_admin = default_site._registry.get(model)
                            if default_admin:
                                # Register with custom site
                                custom_admin_site.register(model, default_admin.__class__)
                                self.stdout.write(f'  ✅ Auto-registered {app_config.label}.{model.__name__}')
                            else:
                                # Register with basic ModelAdmin
                                from django.contrib.admin import ModelAdmin
                                custom_admin_site.register(model, ModelAdmin)
                                self.stdout.write(f'  ✅ Auto-registered {app_config.label}.{model.__name__} (basic)')
                        except Exception as e:
                            self.stdout.write(f'  ❌ Failed to auto-register {app_config.label}.{model.__name__}: {e}')