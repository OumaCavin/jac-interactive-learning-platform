#!/usr/bin/env python3
"""
JAC Learning Platform Backend Setup Script
Complete Django REST Framework backend implementation
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def create_project_structure():
    """Create the complete project structure"""
    
    # Create main project directory
    os.makedirs('jac_learning_platform', exist_ok=True)
    
    # Create apps
    apps = ['users', 'learning', 'agents', 'assessment', 'core']
    for app in apps:
        os.makedirs(f'jac_learning_platform/{app}', exist_ok=True)
        os.makedirs(f'jac_learning_platform/{app}/migrations', exist_ok=True)
        os.makedirs(f'jac_learning_platform/{app}/api', exist_ok=True)
    
    # Create additional directories
    os.makedirs('jac_learning_platform/static', exist_ok=True)
    os.makedirs('jac_learning_platform/media', exist_ok=True)
    os.makedirs('jac_learning_platform/config', exist_ok=True)
    
    print("✅ Project structure created")

def create_requirements():
    """Create requirements.txt with all dependencies"""
    requirements = """Django==4.2.7
djangorestframework==3.14.0
djangorestframework-simplejwt==5.3.0
django-cors-headers==4.3.1
django-filter==23.3
django-extensions==3.2.3
psycopg2-binary==2.9.9
celery==5.3.4
redis==5.0.1
Pillow==10.0.1
django-storages==1.14.2
boto3==1.34.0
python-decouple==3.8
django-environ==0.11.2
"""
    
    with open('requirements.txt', 'w') as f:
        f.write(requirements)
    
    print("✅ Requirements.txt created")

def create_manage_py():
    """Create Django manage.py"""
    content = """#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jac_learning_platform.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
"""
    
    with open('manage.py', 'w') as f:
        f.write(content)
    
    os.chmod('manage.py', 0o755)
    print("✅ manage.py created")

if __name__ == "__main__":
    print("🚀 Setting up JAC Learning Platform Backend...")
    create_project_structure()
    create_requirements()
    create_manage_py()
    print("\n🎉 Basic structure created! Continue with backend implementation...")
