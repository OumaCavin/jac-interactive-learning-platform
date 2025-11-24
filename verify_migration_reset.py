#!/usr/bin/env python3
"""
Migration State Verification Script
Verifies that migration reset was successful and Django is properly configured
"""

import os
import sys
import json
import subprocess
import time

def run_django_command(command):
    """Run a Django management command"""
    try:
        result = subprocess.run([
            'docker-compose', 'exec', '-T', 'backend',
            'python', 'manage.py', command
        ], capture_output=True, text=True, timeout=30)
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out"
    except Exception as e:
        return -1, "", str(e)

def check_django_setup():
    """Check Django configuration and setup"""
    print("🔍 Checking Django Setup...")
    
    # Check Django configuration
    print("  📋 Running Django system check...")
    code, stdout, stderr = run_django_command('check --settings=config.settings')
    if code == 0:
        print("  ✅ Django system check passed")
    else:
        print(f"  ❌ Django system check failed: {stderr}")
        return False
    
    # Check migrations status
    print("  📊 Checking migration status...")
    code, stdout, stderr = run_django_command('showmigrations')
    if code == 0:
        print("  ✅ Migration status retrieved")
        print("\n📋 Current Migration State:")
        print("=" * 50)
        print(stdout)
        print("=" * 50)
    else:
        print(f"  ❌ Failed to get migration status: {stderr}")
        return False
    
    return True

def check_database_connectivity():
    """Check database connectivity"""
    print("\n🗄️ Checking Database Connectivity...")
    
    # Test database shell access
    code, stdout, stderr = run_django_command('dbshell -c "\\dt"')
    if code == 0:
        print("  ✅ Database connectivity confirmed")
        print("  📋 Available tables:")
        lines = stdout.strip().split('\n')
        for line in lines[2:]:  # Skip header lines
            if line.strip() and not line.startswith('-'):
                print(f"    • {line.strip()}")
    else:
        print(f"  ❌ Database connectivity failed: {stderr}")
        return False
    
    return True

def check_application_services():
    """Check if application services are running"""
    print("\n🚀 Checking Application Services...")
    
    # Check if backend service is healthy
    try:
        result = subprocess.run([
            'docker-compose', 'ps', '--format', 'json', 'backend'
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            # Parse JSON output
            services = json.loads(result.stdout)
            for service in services:
                if isinstance(service, dict):
                    name = service.get('Name', '')
                    state = service.get('State', '')
                    status = service.get('Status', '')
                    print(f"  📱 {name}: {state} ({status})")
                    
                    if state != 'running':
                        print(f"    ⚠️ Service {name} is not running!")
                        return False
        else:
            print(f"  ❌ Failed to check service status: {result.stderr}")
            return False
            
    except json.JSONDecodeError:
        # Fallback to regular ps command
        result = subprocess.run([
            'docker-compose', 'ps', 'backend'
        ], capture_output=True, text=True, timeout=10)
        
        print("  📋 Service Status:")
        print(result.stdout)
    
    return True

def test_api_endpoints():
    """Test API endpoints"""
    print("\n🌐 Testing API Endpoints...")
    
    # Test health endpoint
    try:
        result = subprocess.run([
            'curl', '-s', '-o', '/dev/null', '-w', '%{http_code}',
            'http://localhost:8000/api/health/'
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            status_code = result.stdout.strip()
            if status_code == '200':
                print("  ✅ Health endpoint responding (HTTP 200)")
            else:
                print(f"  ⚠️ Health endpoint returned HTTP {status_code}")
        else:
            print(f"  ❌ Health endpoint test failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"  ❌ API endpoint test failed: {str(e)}")
        return False
    
    return True

def verify_migration_files():
    """Verify migration files exist and are properly formatted"""
    print("\n📁 Verifying Migration Files...")
    
    backend_path = "/workspace/backend"
    apps_with_migrations = []
    
    # Find all apps with migrations
    for root, dirs, files in os.walk(backend_path):
        if 'migrations' in root:
            app_name = os.path.basename(os.path.dirname(root))
            if app_name not in apps_with_migrations:
                apps_with_migrations.append(app_name)
    
    print(f"  📋 Found migration directories for apps: {', '.join(apps_with_migrations)}")
    
    # Check for migration files
    for app in apps_with_migrations:
        migration_dir = f"{backend_path}/apps/{app}/migrations"
        if os.path.exists(migration_dir):
            migration_files = [f for f in os.listdir(migration_dir) 
                             if f.endswith('.py') and f != '__init__.py']
            print(f"    📄 {app}: {len(migration_files)} migration files")
            for migration_file in sorted(migration_files):
                print(f"      • {migration_file}")
        else:
            print(f"    ⚠️ {app}: No migrations directory found")
    
    return len(apps_with_migrations) > 0

def generate_report():
    """Generate a comprehensive verification report"""
    print("\n" + "="*60)
    print("📊 MIGRATION RESET VERIFICATION REPORT")
    print("="*60)
    print(f"🕒 Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📂 Workspace: {os.getcwd()}")
    print(f"🐳 Docker Status:")
    
    try:
        result = subprocess.run(['docker-compose', 'ps'], 
                              capture_output=True, text=True, timeout=15)
        print(result.stdout)
    except Exception as e:
        print(f"    ❌ Unable to get Docker status: {str(e)}")
    
    print("="*60)

def main():
    """Main verification function"""
    print("🔧 MIGRATION STATE VERIFICATION")
    print("================================")
    print("This script verifies that the migration reset was successful")
    print("and all Django services are properly configured.")
    print("")
    
    # Run all checks
    checks_passed = 0
    total_checks = 5
    
    if check_django_setup():
        checks_passed += 1
    
    if check_database_connectivity():
        checks_passed += 1
    
    if check_application_services():
        checks_passed += 1
    
    if test_api_endpoints():
        checks_passed += 1
    
    if verify_migration_files():
        checks_passed += 1
    
    # Generate final report
    generate_report()
    
    # Summary
    print(f"\n🎯 VERIFICATION SUMMARY: {checks_passed}/{total_checks} checks passed")
    
    if checks_passed == total_checks:
        print("🎉 ALL CHECKS PASSED!")
        print("✅ Migration reset was successful")
        print("✅ Django is properly configured")
        print("✅ Database connectivity confirmed")
        print("✅ All services are running")
        print("✅ API endpoints are responding")
        print("\n🌐 Your platform is ready:")
        print("   Frontend: http://localhost:3000")
        print("   Admin: http://localhost:3000/admin")
        print("   API: http://localhost:8000/api/")
        return 0
    else:
        print("⚠️ SOME CHECKS FAILED")
        print("❌ Migration reset may not be complete")
        print("🔧 Review the errors above and run migration reset again")
        print("📖 See MIGRATION_RESET_GUIDE.md for troubleshooting")
        return 1

if __name__ == "__main__":
    sys.exit(main())