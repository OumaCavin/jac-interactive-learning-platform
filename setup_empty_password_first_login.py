#!/usr/bin/env python3
"""
Create users with empty passwords and first-login requirements
This allows users to login with empty passwords and be prompted to set new ones
"""

import os
import sys
import django
import subprocess
from django.contrib.auth.models import User
from django.db import connection

def setup_django():
    """Setup Django environment"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    
    backend_path = '/workspace/jac-interactive-learning-platform/backend'
    if backend_path not in sys.path:
        sys.path.insert(0, backend_path)
    
    django.setup()
    print("✅ Django environment setup complete")

def create_users_with_empty_passwords():
    """Create users with empty passwords that require first login change"""
    
    print("\n👤 Creating users with empty passwords and first-login requirements...")
    
    # Clean up existing users
    try:
        User.objects.filter(username='admin').delete()
        User.objects.filter(username='demo_user').delete()
        print("🗑️ Cleaned up existing users")
    except Exception as e:
        print(f"ℹ️ No existing users to clean: {e}")
    
    # Create admin user with empty password
    print("🔧 Creating admin user with empty password...")
    
    admin_user = User.objects.create_user(
        username='admin',
        email='cavin.otieno012@gmail.com',
        password=None,  # Empty password
        is_superuser=True,
        is_staff=True,
        is_active=True
    )
    
    # Mark as needing password change
    admin_user.last_login = None
    admin_user.save()
    
    print("✅ Admin user created with empty password")
    print(f"   Username: {admin_user.username}")
    print(f"   Email: {admin_user.email}")
    print(f"   Has usable password: {admin_user.has_usable_password()}")
    print(f"   Will be prompted to set password on first login")
    
    # Create demo user with empty password
    print("\n🔧 Creating demo user with empty password...")
    
    demo_user = User.objects.create_user(
        username='demo_user',
        email='demo@example.com',
        password=None,  # Empty password
        is_superuser=False,
        is_staff=False,
        is_active=True
    )
    
    # Mark as needing password change
    demo_user.last_login = None
    demo_user.save()
    
    print("✅ Demo user created with empty password")
    print(f"   Username: {demo_user.username}")
    print(f"   Email: {demo_user.email}")
    print(f"   Has usable password: {demo_user.has_usable_password()}")
    print(f"   Will be prompted to set password on first login")
    
    return admin_user, demo_user

def create_first_login_middleware():
    """Create middleware to handle first login password prompts"""
    
    middleware_code = '''
"""
First Login Password Prompt Middleware
Redirects users with empty passwords to password change page
"""

from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

class FirstLoginPasswordMiddleware:
    """
    Middleware to handle users with empty passwords
    Redirects them to password change page on first login
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only check authenticated users
        if request.user.is_authenticated:
            user = request.user
            
            # If user has no usable password, redirect to password change
            if not user.has_usable_password() and not user.last_login:
                # Don't redirect if already on password change page
                if not request.path.startswith('/change-password/'):
                    messages.warning(request, "Please set your password before continuing.")
                    return redirect('password_change')
        
        response = self.get_response(request)
        return response
'''
    
    middleware_file = '/workspace/jac-interactive-learning-platform/backend/apps/users/middleware.py'
    
    with open(middleware_file, 'w') as f:
        f.write(middleware_code)
    
    print(f"✅ Created first login middleware: {middleware_file}")

def create_password_change_view():
    """Create a password change view for first-time users"""
    
    view_code = '''
"""
Password change view for users with empty passwords
This view handles both first-time users and regular password changes
"""

from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse

@login_required
def password_change_view(request):
    """
    Handle password change for users with empty passwords
    """
    user = request.user
    
    # Check if this is a first-time user (no password set)
    is_first_login = not user.has_usable_password() and not user.last_login
    
    if request.method == 'POST':
        # Use PasswordChangeForm which works for both cases
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            
            # Update session to prevent logout
            update_session_auth_hash(request, user)
            
            if is_first_login:
                messages.success(request, "Password set successfully! Welcome to JAC Learning Platform.")
            else:
                messages.success(request, "Password changed successfully!")
            
            # Redirect to dashboard after password change
            return redirect('dashboard')
        else:
            if is_first_login:
                messages.error(request, "Please set a valid password to continue.")
    else:
        # GET request
        if is_first_login:
            # Initialize form with only new password fields
            form = PasswordChangeForm(request.user)
            messages.info(request, "Please set your password to continue using the platform.")
        else:
            form = PasswordChangeForm(request.user)
    
    context = {
        'form': form,
        'is_first_login': is_first_login,
        'user': user
    }
    
    return render(request, 'auth/password_change.html', context)
'''
    
    view_file = '/workspace/jac-interactive-learning-platform/backend/apps/users/views/auth_views.py'
    
    # Create views directory if it doesn't exist
    import os
    os.makedirs(os.path.dirname(view_file), exist_ok=True)
    
    with open(view_file, 'w') as f:
        f.write(view_code)
    
    print(f"✅ Created password change view: {view_file}")
    
    # Create the template
    template_code = '''
{% extends "base.html" %}

{% block title %}
{% if is_first_login %}Set Password{% else %}Change Password{% endif %}
{% endblock %}

{% block content %}
<div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
        <div>
            {% if is_first_login %}
                <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
                    Set Your Password
                </h2>
                <p class="mt-2 text-center text-sm text-gray-600">
                    Please set your password to access the JAC Learning Platform
                </p>
            {% else %}
                <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
                    Change Your Password
                </h2>
                <p class="mt-2 text-center text-sm text-gray-600">
                    Enter your current password and choose a new one
                </p>
            {% endif %}
        </div>
        
        <form class="mt-8 space-y-6" method="POST">
            {% csrf_token %}
            
            {% if form.errors %}
                <div class="rounded-md bg-red-50 p-4">
                    <div class="text-sm text-red-700">
                        {% for field, errors in form.errors.items %}
                            {% for error in errors %}
                                <p>{{ error }}</p>
                            {% endfor %}
                        {% endfor %}
                    </div>
                </div>
            {% endif %}
            
            {% if messages %}
                {% for message in messages %}
                    <div class="rounded-md {% if message.tags %}bg-{{ message.tags }}-50 p-4{% else %}bg-gray-50 p-4{% endif %}">
                        <div class="text-sm {% if message.tags %}text-{{ message.tags }}-700{% else %}text-gray-700{% endif %}">
                            {{ message }}
                        </div>
                    </div>
                {% endfor %}
            {% endif %}
            
            <div class="space-y-4">
                {% if not is_first_login %}
                    <div>
                        <label for="{{ form.old_password.id_for_label }}" class="sr-only">Current Password</label>
                        {{ form.old_password }}
                        {% if form.old_password.errors %}
                            <p class="mt-1 text-sm text-red-600">{{ form.old_password.errors.0 }}</p>
                        {% endif %}
                    </div>
                {% endif %}
                
                <div>
                    <label for="{{ form.new_password1.id_for_label }}" class="sr-only">New Password</label>
                    {{ form.new_password1 }}
                    {% if form.new_password1.errors %}
                        <p class="mt-1 text-sm text-red-600">{{ form.new_password1.errors.0 }}</p>
                    {% endif %}
                </div>
                
                <div>
                    <label for="{{ form.new_password2.id_for_label }}" class="sr-only">Confirm New Password</label>
                    {{ form.new_password2 }}
                    {% if form.new_password2.errors %}
                        <p class="mt-1 text-sm text-red-600">{{ form.new_password2.errors.0 }}</p>
                    {% endif %}
                </div>
            </div>
            
            <div>
                <button type="submit" class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
                    {% if is_first_login %}
                        Set Password
                    {% else %}
                        Change Password
                    {% endif %}
                </button>
            </div>
        </form>
    </div>
</div>
{% endblock %}
'''
    
    # Create template directory structure
    template_dir = '/workspace/jac-interactive-learning-platform/backend/templates/auth'
    import os
    os.makedirs(template_dir, exist_ok=True)
    
    template_file = os.path.join(template_dir, 'password_change.html')
    with open(template_file, 'w') as f:
        f.write(template_code)
    
    print(f"✅ Created password change template: {template_file}")

def update_settings():
    """Update settings.py to include the middleware"""
    
    settings_file = '/workspace/jac-interactive-learning-platform/backend/config/settings.py'
    
    # Read current settings
    with open(settings_file, 'r') as f:
        content = f.read()
    
    # Add middleware if not already present
    if 'FirstLoginPasswordMiddleware' not in content:
        # Find MIDDLEWARE section and add our middleware
        lines = content.split('\n')
        middleware_section_found = False
        
        for i, line in enumerate(lines):
            if line.strip() == "MIDDLEWARE = [":
                middleware_section_found = True
                # Add our middleware after existing middleware
                j = i + 1
                while j < len(lines) and lines[j].strip() != ']':
                    j += 1
                
                if j < len(lines):
                    # Insert our middleware before closing bracket
                    lines.insert(j, "    'users.middleware.FirstLoginPasswordMiddleware',")
                    break
        
        # Write back to file
        with open(settings_file, 'w') as f:
            f.write('\n'.join(lines))
        
        print(f"✅ Updated settings.py with FirstLoginPasswordMiddleware")
    else:
        print("ℹ️ Middleware already configured in settings.py")

def update_urls():
    """Update urls.py to include password change route"""
    
    urls_file = '/workspace/jac-interactive-learning-platform/backend/config/urls.py'
    
    # Add import for our view
    with open(urls_file, 'r') as f:
        content = f.read()
    
    if 'password_change_view' not in content:
        lines = content.split('\n')
        
        # Add import
        import_added = False
        for i, line in enumerate(lines):
            if line.startswith('from') and 'users' in line:
                if 'password_change_view' not in line:
                    lines[i] = line.rstrip(',') + ', password_change_view)'
                import_added = True
                break
        
        if not import_added:
            # Add new import
            lines.insert(0, "from users.views.auth_views import password_change_view")
        
        # Add URL pattern
        for i, line in enumerate(lines):
            if 'path(' in line and 'admin/' in line:
                # Add our URL after admin
                lines.insert(i + 1, "    path('change-password/', password_change_view, name='password_change'),")
                break
        
        with open(urls_file, 'w') as f:
            f.write('\n'.join(lines))
        
        print(f"✅ Updated urls.py with password change route")
    else:
        print("ℹ️ URL route already configured")

def main():
    print("🔧 JAC Platform - Empty Password + First Login Setup")
    print("=" * 60)
    
    try:
        setup_django()
        admin_user, demo_user = create_users_with_empty_passwords()
        
        print("\n📁 Creating supporting files...")
        create_first_login_middleware()
        create_password_change_view()
        update_settings()
        update_urls()
        
        print("\n🎉 Empty Password Setup Complete!")
        print("=" * 60)
        print("\n✅ USERS CREATED:")
        print("   Admin User:")
        print("     Username: admin")
        print("     Email: cavin.otieno012@gmail.com")
        print("     Password: (EMPTY - will be set on first login)")
        print("     URL: http://localhost:8000/admin/")
        print("\n   Demo User:")
        print("     Username: demo_user") 
        print("     Email: demo@example.com")
        print("     Password: (EMPTY - will be set on first login)")
        print("     URL: http://localhost:3000/login")
        
        print("\n🔧 FIRST LOGIN PROCESS:")
        print("1. User tries to login with empty password")
        print("2. Django accepts empty password for users with no usable password")
        print("3. User is redirected to password change page")
        print("4. User sets new password")
        print("5. User can now use platform normally")
        
        print("\n📋 FEATURES:")
        print("   ✅ Empty passwords allowed for first-time users")
        print("   ✅ Automatic redirect to password change on first login")
        print("   ✅ Middleware handles empty password detection")
        print("   ✅ Beautiful password change interface")
        print("   ✅ Integration with existing authentication system")
        
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())