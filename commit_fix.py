#!/usr/bin/env python3
import subprocess
import os

os.chdir('/workspace')

try:
    # Check git status
    result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True, timeout=30)
    
    if result.stdout.strip():
        print('Changes detected:')
        print(result.stdout)
        
        # Add all changes
        subprocess.run(['git', 'add', '.'], timeout=10)
        
        # Commit
        result = subprocess.run(['git', 'commit', '-m', 'Fix: Remove duplicate agents URL namespace conflict'], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print('✅ Changes committed successfully')
            print(result.stdout)
        else:
            print('❌ Commit failed:')
            print(result.stderr)
    else:
        print('No changes to commit')

    # Push to remote
    print('Pushing to remote...')
    result = subprocess.run(['git', 'push', 'origin', 'main'], 
                          capture_output=True, text=True, timeout=60)
    if result.returncode == 0:
        print('✅ Changes pushed successfully')
        print(result.stdout)
    else:
        print('❌ Push failed:')
        print(result.stderr)

except Exception as e:
    print(f'Error: {e}')