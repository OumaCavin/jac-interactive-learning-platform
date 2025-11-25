#!/usr/bin/env python3
"""
Check Git status and file changes for the JAC Learning Platform
"""

import subprocess
import os

def run_git_command(command, description):
    """Run a Git command and return the result"""
    try:
        print(f"\n{'='*60}")
        print(f"RUNNING: {description}")
        print(f"COMMAND: {command}")
        print(f"{'='*60}")
        
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True,
            timeout=30
        )
        
        print(f"EXIT CODE: {result.returncode}")
        print(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            print(f"STDERR:\n{result.stderr}")
            
        return result
    except subprocess.TimeoutExpired:
        print(f"TIMEOUT: Command took too long")
        return None
    except Exception as e:
        print(f"ERROR: {e}")
        return None

def main():
    print("🔍 Git Status Check for JAC Learning Platform")
    print("=" * 60)
    
    # Check current branch
    run_git_command("git rev-parse --abbrev-ref HEAD", "Current Branch")
    
    # Check remotes
    run_git_command("git remote -v", "Remote Configuration")
    
    # Check status
    run_git_command("git status --porcelain", "Git Status (porcelain)")
    
    # Check if backend/apps/learning/__init__.py is modified
    init_file = "/workspace/backend/apps/learning/__init__.py"
    if os.path.exists(init_file):
        with open(init_file, 'r') as f:
            content = f.read()
            if "Author: Cavin Otieno" in content:
                print("\n✅ CONFIRMED: backend/apps/learning/__init__.py contains 'Author: Cavin Otieno'")
            elif "Author: Cavin Otieno" in content:
                print("\n❌ ERROR: backend/apps/learning/__init__.py still contains 'Author: Cavin Otieno'")
            else:
                print("\n⚠️  WARNING: No author line found in backend/apps/learning/__init__.py")
    
    # Check for uncommitted changes
    run_git_command("git diff --stat", "Uncommitted Changes")
    
    # Check recent commits
    run_git_command("git log --oneline -3 --no-pager", "Recent Commits")
    
    # Try to check remote status
    run_git_command("git fetch origin --dry-run", "Remote Status Check")
    
    print(f"\n{'='*60}")
    print("✅ Git status check completed")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()