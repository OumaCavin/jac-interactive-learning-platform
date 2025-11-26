#!/usr/bin/env python3
import os
import subprocess

# Completely clean environment
clean_env = {
    'PATH': os.environ.get('PATH', ''),
    'HOME': os.environ.get('HOME', ''),
    # Remove all Django-related variables
}

# Change to a non-Django directory
os.chdir('/')

def run_cmd(cmd):
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            env=clean_env,
            cwd='/workspace',
            timeout=5
        )
        return result.stdout, result.stderr, result.returncode
    except:
        return "", "timeout", 1

print("=== Checking Git History ===")

# Try git log with git-dir specified
stdout, stderr, code = run_cmd("git --git-dir=/workspace/.git --work-tree=/workspace log --oneline -10")

if code == 0 and stdout:
    print("Recent commits found:")
    print(stdout)
    
    # Check for problematic messages
    lines = [line.strip() for line in stdout.split('\n') if line.strip()]
    problematic = []
    for line in lines:
        if any(x in line.lower() for x in ['message', 'sync', 'system check']):
            problematic.append(line)
    
    if problematic:
        print("\n=== FOUND PROBLEMATIC COMMIT MESSAGES ===")
        for msg in problematic:
            print(f"  - {msg}")
    else:
        print("\n=== All commit messages look human-readable ===")
else:
    print(f"Error: {stderr}")

# Check current status
stdout, stderr, code = run_cmd("git --git-dir=/workspace/.git --work-tree=/workspace status --porcelain")
if code == 0:
    if stdout.strip():
        print("\n=== Working tree changes ===")
        print(stdout)
    else:
        print("\n=== Working tree is clean ===")