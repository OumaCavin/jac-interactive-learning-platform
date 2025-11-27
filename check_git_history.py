#!/usr/bin/env python3
"""
Check Git history and identify problematic commit messages
"""
import subprocess
import sys
import os

# Change to workspace directory
os.chdir('/workspace')

# Set minimal environment to avoid Django
env = os.environ.copy()
env.pop('DJANGO_SETTINGS_MODULE', None)
env.pop('PYTHONPATH', None)

def run_git_command(cmd):
    """Run git command with minimal environment"""
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            capture_output=True, 
            text=True, 
            env=env,
            timeout=10
        )
        return result.stdout, result.stderr, result.returncode
    except subprocess.TimeoutExpired:
        return "", "Command timed out", 1
    except Exception as e:
        return "", str(e), 1

def main():
    print("=== Checking Git History ===")
    
    # Check recent commits
    stdout, stderr, code = run_git_command("git log --oneline -20")
    
    if code == 0:
        print("Recent commits:")
        print(stdout)
        
        # Look for system-generated messages
        lines = stdout.split('\n')
        problematic = []
        for i, line in enumerate(lines):
            if any(pattern in line for pattern in [
                'Message', 'message', 'Sync with matrix', 
                'Message 338153140736182', 'System check'
            ]):
                problematic.append(f"Line {i}: {line}")
        
        if problematic:
            print("\n=== Problematic Commit Messages Found ===")
            for msg in problematic:
                print(msg)
        else:
            print("\n=== No obviously problematic commit messages found ===")
    else:
        print(f"Error checking git log: {stderr}")
    
    # Check current branch
    stdout, stderr, code = run_git_command("git branch --show-current")
    if code == 0:
        print(f"\nCurrent branch: {stdout.strip()}")
    
    # Check remote status
    stdout, stderr, code = run_git_command("git remote -v")
    if code == 0:
        print(f"\nRemotes:\n{stdout}")

if __name__ == "__main__":
    main()