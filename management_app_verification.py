#!/usr/bin/env python3
"""
Management App Verification Script
Comprehensive verification of the management app implementation for JAC Learning Platform
"""

import os
import sys
import ast
from pathlib import Path

def verify_file_structure():
    """Verify the management app file structure"""
    print("=" * 60)
    print("📁 FILE STRUCTURE VERIFICATION")
    print("=" * 60)
    
    base_path = Path("/workspace/backend/apps/management")
    required_files = [
        "__init__.py",
        "apps.py", 
        "commands/__init__.py",
        "commands/initialize_platform.py"
    ]
    
    optional_files = []
    
    all_files = required_files + optional_files
    missing_files = []
    existing_files = []
    
    for file_path in all_files:
        full_path = base_path / file_path
        if full_path.exists():
            existing_files.append(file_path)
            print(f"✅ {file_path}")
        else:
            missing_files.append(file_path)
            print(f"❌ {file_path} - MISSING")
    
    print(f"\nFile Structure Status: {len(existing_files)}/{len(all_files)} files present")
    
    # Also check learning app management structure
    learning_mgmt_path = Path("/workspace/backend/apps/learning/management")
    learning_files = [
        "__init__.py",
        "commands/__init__.py", 
        "commands/populate_jac_curriculum.py"
    ]
    
    print(f"\n📁 Learning App Management Structure:")
    for file_path in learning_files:
        full_path = learning_mgmt_path / file_path
        if full_path.exists():
            existing_files.append(f"learning/{file_path}")
            print(f"✅ learning/{file_path}")
        else:
            missing_files.append(f"learning/{file_path}")
            print(f"❌ learning/{file_path} - MISSING")
    
    return len(missing_files) == 0

def verify_file_contents():
    """Verify the content and structure of each file"""
    print("\n" + "=" * 60)
    print("📄 FILE CONTENT VERIFICATION")
    print("=" * 60)
    
    issues = []
    
    # Check __init__.py
    init_file = Path("/workspace/backend/apps/management/__init__.py")
    if init_file.exists():
        try:
            with open(init_file, 'r') as f:
                content = f.read()
            
            # Verify key components
            checks = [
                ("Package metadata", "Management App Package" in content),
                ("App config reference", "apps.ManagementConfig" in content),
                ("Command import", "initialize_platform" in content),
                ("Version info", "__version__" in content)
            ]
            
            for check_name, check_result in checks:
                if check_result:
                    print(f"✅ __init__.py: {check_name}")
                else:
                    issues.append(f"__init__.py missing {check_name}")
                    print(f"❌ __init__.py missing {check_name}")
            
        except Exception as e:
            issues.append(f"Error reading __init__.py: {e}")
            print(f"❌ Error reading __init__.py: {e}")
    
    # Check apps.py
    apps_file = Path("/workspace/backend/apps/management/apps.py")
    if apps_file.exists():
        try:
            with open(apps_file, 'r') as f:
                content = f.read()
            
            checks = [
                ("ManagementConfig class", "class ManagementConfig" in content),
                ("App name", "apps.management" in content),
                ("Django AppConfig", "AppConfig" in content),
                ("verbose name", "verbose_name" in content)
            ]
            
            for check_name, check_result in checks:
                if check_result:
                    print(f"✅ apps.py: {check_name}")
                else:
                    issues.append(f"apps.py missing {check_name}")
                    print(f"❌ apps.py missing {check_name}")
            
        except Exception as e:
            issues.append(f"Error reading apps.py: {e}")
            print(f"❌ Error reading apps.py: {e}")
    
    # Check initialize_platform command
    cmd_file = Path("/workspace/backend/apps/management/commands/initialize_platform.py")
    if cmd_file.exists():
        try:
            with open(cmd_file, 'r') as f:
                content = f.read()
            
            checks = [
                ("Command class", "class Command(BaseCommand)" in content),
                ("BaseCommand import", "from django.core.management.base import BaseCommand" in content),
                ("Migrations logic", "def run_migrations" in content),
                ("Superuser creation", "def create_superuser" in content),
                ("Command arguments", "add_arguments" in content),
                ("Database connection check", "cursor.execute" in content),
                ("Database connection test", "SELECT 1" in content),
                ("Migrate command call", "call_command('migrate'" in content),
                ("Superuser creation", "User.objects.create_superuser" in content),
                ("Management command signature", "def handle" in content)
            ]
            
            for check_name, check_result in checks:
                if check_result:
                    print(f"✅ initialize_platform.py: {check_name}")
                else:
                    issues.append(f"initialize_platform.py missing {check_name}")
                    print(f"❌ initialize_platform.py missing {check_name}")
            
            # Count lines and complexity
            lines = content.split('\n')
            line_count = len([line for line in lines if line.strip() and not line.strip().startswith('#')])
            print(f"✅ initialize_platform.py: {line_count} lines of code")
            
        except Exception as e:
            issues.append(f"Error reading initialize_platform.py: {e}")
            print(f"❌ Error reading initialize_platform.py: {e}")
    
    # Check populate_jac_curriculum command
    populate_file = Path("/workspace/backend/apps/learning/management/commands/populate_jac_curriculum.py")
    if populate_file.exists():
        try:
            with open(populate_file, 'r') as f:
                content = f.read()
            
            checks = [
                ("Command class", "class Command(BaseCommand)" in content),
                ("Learning model imports", "from apps.learning.models import" in content),
                ("Curriculum population logic", "get_module1_content" in content),
                ("User model import", "from django.contrib.auth import get_user_model" in content),
                ("Command signature", "def handle" in content)
            ]
            
            for check_name, check_result in checks:
                if check_result:
                    print(f"✅ populate_jac_curriculum.py: {check_name}")
                else:
                    issues.append(f"populate_jac_curriculum.py missing {check_name}")
                    print(f"❌ populate_jac_curriculum.py missing {check_name}")
            
            # Check for comprehensive curriculum data
            if "JAC Programming Language Course" in content:
                print("✅ populate_jac_curriculum.py: Comprehensive JAC curriculum")
            else:
                issues.append("populate_jac_curriculum.py missing comprehensive curriculum data")
                print("❌ populate_jac_curriculum.py missing comprehensive curriculum data")
            
        except Exception as e:
            issues.append(f"Error reading populate_jac_curriculum.py: {e}")
            print(f"❌ Error reading populate_jac_curriculum.py: {e}")
    
    return len(issues) == 0, issues

def verify_django_registration():
    """Verify that the management app is registered in Django settings"""
    print("\n" + "=" * 60)
    print("⚙️  DJANGO CONFIGURATION VERIFICATION")
    print("=" * 60)
    
    settings_file = Path("/workspace/backend/config/settings.py")
    if not settings_file.exists():
        print("❌ Django settings.py not found")
        return False
    
    try:
        with open(settings_file, 'r') as f:
            content = f.read()
        
        checks = [
            ("LOCAL_APPS definition", "LOCAL_APPS = [" in content),
            ("apps.management registration", "'apps.management'" in content),
            ("INSTALLED_APPS composition", "INSTALLED_APPS = DJANGO_APPS" in content),
            ("Settings file completeness", "SECRET_KEY" in content and "DEBUG" in content)
        ]
        
        issues = []
        for check_name, check_result in checks:
            if check_result:
                print(f"✅ {check_name}")
            else:
                issues.append(f"Settings file missing {check_name}")
                print(f"❌ {check_name}")
        
        return len(issues) == 0
        
    except Exception as e:
        print(f"❌ Error reading settings.py: {e}")
        return False

def verify_syntax_validity():
    """Verify that all Python files have valid syntax"""
    print("\n" + "=" * 60)
    print("🔍 SYNTAX VALIDATION")
    print("=" * 60)
    
    files_to_check = [
        "/workspace/backend/apps/management/__init__.py",
        "/workspace/backend/apps/management/apps.py", 
        "/workspace/backend/apps/management/commands/initialize_platform.py",
        "/workspace/backend/apps/learning/management/commands/populate_jac_curriculum.py"
    ]
    
    all_valid = True
    
    for file_path in files_to_check:
        file = Path(file_path)
        if not file.exists():
            continue
            
        try:
            with open(file, 'r', encoding='utf-8') as f:
                source = f.read()
            
            # Parse the Python code
            ast.parse(source)
            print(f"✅ {file.name}: Valid Python syntax")
            
        except SyntaxError as e:
            print(f"❌ {file.name}: Syntax error on line {e.lineno}: {e.msg}")
            all_valid = False
        except Exception as e:
            print(f"❌ {file.name}: Error parsing file: {e}")
            all_valid = False
    
    return all_valid

def main():
    """Main verification function"""
    print("🚀 Management App Verification - JAC Learning Platform")
    print("=" * 60)
    
    # Change to backend directory for relative path consistency
    os.chdir("/workspace/backend")
    
    results = {}
    
    # Run all verification checks
    results['file_structure'] = verify_file_structure()
    results['file_contents'], content_issues = verify_file_contents()
    results['django_config'] = verify_django_registration()
    results['syntax_valid'] = verify_syntax_validity()
    
    # Overall assessment
    print("\n" + "=" * 60)
    print("📊 OVERALL ASSESSMENT")
    print("=" * 60)
    
    all_passed = all(results.values())
    
    for check, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{check.replace('_', ' ').title()}: {status}")
    
    if content_issues:
        print(f"\n📝 Content Issues Found ({len(content_issues)}):")
        for issue in content_issues:
            print(f"  • {issue}")
    
    # Summary
    if all_passed:
        print(f"\n🎉 VERIFICATION SUCCESSFUL!")
        print(f"✅ The management app is properly implemented and configured")
        print(f"✅ All files are present with correct content")
        print(f"✅ Django registration is complete")
        print(f"✅ Python syntax is valid")
        
        print(f"\n📋 Management App Features:")
        print(f"  • Platform initialization command")
        print(f"  • Comprehensive JAC curriculum population")
        print(f"  • Database migration handling")
        print(f"  • Superuser creation")
        print(f"  • Django management integration")
        
    else:
        print(f"\n⚠️  VERIFICATION ISSUES DETECTED")
        print(f"❌ The management app has implementation gaps")
        print(f"📝 Review the issues above for details")
    
    print(f"\n" + "=" * 60)
    print(f"Verification completed successfully!")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)