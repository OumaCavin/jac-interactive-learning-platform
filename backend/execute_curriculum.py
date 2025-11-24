#!/usr/bin/env python3
"""
Execute Django management command to populate curriculum
"""

import os
import sys
import signal
import subprocess
import time

def run_management_command():
    """Run the Django management command to populate curriculum"""
    
    # Kill any existing Django processes first
    print("🧹 Cleaning up existing processes...")
    try:
        subprocess.run(['pkill', '-f', 'python'], capture_output=True)
        subprocess.run(['pkill', '-f', 'runserver'], capture_output=True)
        time.sleep(2)
    except:
        pass
    
    # Set environment
    os.environ['PYTHONPATH'] = '/workspace/backend'
    os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
    
    # Run the management command
    print("🚀 Running Django management command...")
    
    try:
        cmd = [
            '/tmp/.venv/bin/python', 
            '/workspace/backend/manage.py', 
            'populate_jac_curriculum'
        ]
        
        result = subprocess.run(
            cmd, 
            cwd='/workspace/backend',
            capture_output=True, 
            text=True, 
            timeout=60,
            env=os.environ.copy()
        )
        
        print("📋 Command Output:")
        print("=" * 60)
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        print("=" * 60)
        
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print("❌ Command timed out")
        return False
    except Exception as e:
        print(f"❌ Error running command: {e}")
        return False

def verify_database():
    """Verify the curriculum data was populated"""
    print("\n🔍 Verifying database...")
    
    try:
        # Simple Django check without complex imports
        import django
        from django.conf import settings
        
        sys.path.insert(0, '/workspace/backend')
        os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings_minimal'
        
        django.setup()
        
        from apps.learning.models import LearningPath, Module, Lesson, Assessment
        
        # Count records
        paths = LearningPath.objects.count()
        modules = Module.objects.count()
        lessons = Lesson.objects.count()
        assessments = Assessment.objects.count()
        
        print(f"📊 Database Verification:")
        print(f"  Learning Paths: {paths}")
        print(f"  Modules: {modules}")
        print(f"  Lessons: {lessons}")
        print(f"  Assessments: {assessments}")
        
        if paths > 0:
            print("\n✅ Data successfully populated!")
            return True
        else:
            print("\n❌ No data found in database")
            return False
            
    except Exception as e:
        print(f"❌ Verification failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🎯 JAC Curriculum Population")
    print("=" * 40)
    
    # Run the population script
    success = run_management_command()
    
    if success:
        print("✅ Management command completed")
        
        # Verify the data
        verify_database()
        
    else:
        print("❌ Management command failed")
    
    print("\n🏁 Process completed")