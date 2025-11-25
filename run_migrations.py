#!/usr/bin/env python3
import subprocess
import sys
import time

def answer_migration_prompts():
    """Answer migration prompts automatically"""
    
    print("Running migrations and answering prompts automatically...")
    
    # Commands to run with automatic yes answers
    commands = [
        ("makemigrations", ["yes"]),  # Answer 'yes' to last_assessment -> last_difficulty_change
        ("migrate", ["yes"])  # Apply migrations
    ]
    
    for cmd_name, answers in commands:
        try:
            print(f"Running: python manage.py {cmd_name}")
            
            # For makemigrations, answer the prompt
            if cmd_name == "makemigrations":
                proc = subprocess.Popen(
                    ["python", "manage.py", cmd_name],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    cwd="/workspace/backend"
                )
                
                # Send 'yes' answer
                stdout, stderr = proc.communicate(input="yes\n", timeout=30)
                
                print(f"STDOUT: {stdout}")
                print(f"STDERR: {stderr}")
                print(f"Return code: {proc.returncode}")
                
            else:
                # For migrate, run without prompts
                result = subprocess.run(
                    ["python", "manage.py", cmd_name],
                    capture_output=True,
                    text=True,
                    timeout=60,
                    cwd="/workspace/backend"
                )
                
                print(f"STDOUT: {result.stdout}")
                print(f"STDERR: {result.stderr}")
                print(f"Return code: {result.returncode}")
                
        except subprocess.TimeoutExpired:
            print(f"Command {cmd_name} timed out")
        except Exception as e:
            print(f"Error running {cmd_name}: {e}")

if __name__ == "__main__":
    answer_migration_prompts()