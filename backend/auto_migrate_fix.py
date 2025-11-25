#!/usr/bin/env python3
"""
Script to handle Django migration interactive prompt automatically.
This resolves the 'Was spacedrepetitionsession.easiness_factor renamed to spacedrepetitionsession.ease_factor' issue.
"""

import os
import sys
import subprocess
import time
from threading import Thread
from queue import Queue

def handle_prompt_output(output_queue):
    """Read output and send 'y' when prompted"""
    while True:
        try:
            output = sys.stdout.read(1)
            if not output:
                break
            sys.stdout.write(output)
            sys.stdout.flush()
            
            # Check if we see the prompt
            if 'Was spacedrepetitionsession.easiness_factor renamed' in output or '[y/N]' in output:
                sys.stdout.write('y\n')
                sys.stdout.flush()
        except:
            break

def run_migration_with_auto_answer():
    """Run migration with automatic 'yes' answer"""
    
    # Change to backend directory
    os.chdir('/workspace/backend')
    
    # Command to run migrations
    cmd = [sys.executable, 'manage.py', 'migrate', '--noinput']
    
    print("Running Django migrations with automatic 'yes' answers...")
    print("Command:", ' '.join(cmd))
    
    try:
        # Start the migration process
        process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        
        # Send 'y' automatically when prompted
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())
                # If we see the prompt, send 'y'
                if 'Was spacedrepetitionsession.easiness_factor renamed' in output or '[y/N]' in output:
                    process.stdin.write('y\n')
                    process.stdin.flush()
        
        process.wait()
        return process.returncode
        
    except Exception as e:
        print(f"Error running migration: {e}")
        return 1

if __name__ == "__main__":
    exit_code = run_migration_with_auto_answer()
    sys.exit(exit_code)