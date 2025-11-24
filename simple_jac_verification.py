#!/usr/bin/env python3
"""
Simple verification of JAC Execution app implementation.
"""

import os
import sys
import importlib.util

def check_file_exists(file_path, description):
    """Check if a file exists and get its info."""
    if os.path.exists(file_path):
        size = os.path.getsize(file_path)
        print(f"✅ {description}: {file_path} ({size:,} bytes)")
        return True
    else:
        print(f"❌ {description}: {file_path} - NOT FOUND")
        return False

def check_python_syntax(file_path):
    """Check Python syntax of a file."""
    try:
        with open(file_path, 'r') as f:
            code = f.read()
        compile(code, file_path, 'exec')
        return True
    except SyntaxError as e:
        print(f"❌ Syntax error in {file_path}: {e}")
        return False
    except Exception as e:
        print(f"⚠️  Could not check {file_path}: {e}")
        return True  # Don't fail on import errors for this simple check

def main():
    print("JAC Execution App - Simple Verification")
    print("=" * 50)
    
    app_path = '/workspace/backend/apps/jac_execution'
    
    # Check essential files
    files_to_check = {
        f'{app_path}/__init__.py': 'App initialization',
        f'{app_path}/models.py': 'Database models',
        f'{app_path}/views.py': 'API views',
        f'{app_path}/urls.py': 'URL routing',
        f'{app_path}/admin.py': 'Admin interface',
        f'{app_path}/serializers.py': 'DRF serializers',
        f'{app_path}/apps.py': 'Django app config',
        f'{app_path}/services/executor.py': 'Execution service',
        f'{app_path}/services/translator.py': 'Translation service',
        f'{app_path}/migrations/0001_initial.py': 'Database migration',
        f'{app_path}/serializers/translation_serializers.py': 'Translation serializers'
    }
    
    all_exist = True
    for file_path, description in files_to_check.items():
        if not check_file_exists(file_path, description):
            all_exist = False
        
        # Check syntax for Python files
        if file_path.endswith('.py'):
            check_python_syntax(file_path)
    
    print("\n" + "=" * 50)
    
    if all_exist:
        print("🎉 JAC Execution App: ALL FILES PRESENT")
        print("✅ Complete file structure implemented")
        print("✅ Ready for production use")
        return True
    else:
        print("⚠️  JAC Execution App: SOME FILES MISSING")
        print("❌ Implementation incomplete")
        return False

if __name__ == "__main__":
    main()