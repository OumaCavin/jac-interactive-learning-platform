#!/usr/bin/env python3
"""
Direct runner for curriculum population with output capture.
"""

import subprocess
import sys
import time

def run_curriculum_population():
    """Run the curriculum population script and capture output."""
    
    print("🚀 Starting curriculum population...")
    
    try:
        # Run the populate_curriculum.py script
        result = subprocess.run([
            sys.executable, '/workspace/backend/populate_curriculum.py'
        ], capture_output=True, text=True, timeout=120)
        
        print("📋 Script Output:")
        print("=" * 60)
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        print("=" * 60)
        
        print(f"✅ Script completed with return code: {result.returncode}")
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print("❌ Script timed out after 120 seconds")
        return False
    except Exception as e:
        print(f"❌ Error running script: {e}")
        return False

if __name__ == "__main__":
    success = run_curriculum_population()
    
    if success:
        print("\n✅ Curriculum population script executed successfully!")
        
        # Now try to verify the data
        print("\n🔍 Verifying data...")
        try:
            verify_result = subprocess.run([
                sys.executable, '/workspace/backend/verify_curriculum.py'
            ], capture_output=True, text=True, timeout=30)
            
            if verify_result.returncode == 0:
                print("📊 Verification Results:")
                print(verify_result.stdout)
            else:
                print("⚠️  Verification failed")
                print(verify_result.stderr)
                
        except Exception as e:
            print(f"⚠️  Could not verify data: {e}")
    else:
        print("❌ Curriculum population failed!")
    
    sys.exit(0 if success else 1)