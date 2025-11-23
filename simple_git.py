#!/usr/bin/env python3
import subprocess
import os

os.chdir('/workspace')

# Simple git operations
commands = [
    ('git add .', 'Adding changes'),
    ('git status --porcelain', 'Checking status'),
]

for cmd, desc in commands:
    print(f"Running: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        print(f"Return code: {result.returncode}")
        if result.stdout:
            print(f"Output: {result.stdout}")
        if result.stderr:
            print(f"Error: {result.stderr}")
    except Exception as e:
        print(f"Exception: {e}")
    print("-" * 40)