#!/usr/bin/env python3
import os
import sys

# Add only essential paths
sys.path = [p for p in sys.path if 'workspace' not in p and 'jac' not in p.lower()]

def check_git_direct():
    """Check Git history by directly reading git objects"""
    git_dir = '/workspace/.git'
    
    if not os.path.exists(git_dir):
        print("No .git directory found")
        return
    
    try:
        # Read HEAD reference
        head_file = os.path.join(git_dir, 'HEAD')
        if os.path.exists(head_file):
            with open(head_file, 'r') as f:
                head_ref = f.read().strip()
            print(f"HEAD reference: {head_ref}")
        
        # List recent commits by reading refs
        refs_dir = os.path.join(git_dir, 'refs', 'heads')
        if os.path.exists(refs_dir):
            branches = os.listdir(refs_dir)
            print(f"Branches: {branches}")
            
            for branch in branches:
                branch_file = os.path.join(refs_dir, branch)
                with open(branch_file, 'r') as f:
                    commit_hash = f.read().strip()
                print(f"Branch {branch}: {commit_hash}")
        
        # Check logs directory for commit messages
        logs_dir = os.path.join(git_dir, 'logs')
        if os.path.exists(logs_dir):
            print("\n=== Recent commit messages from logs ===")
            reflog_file = os.path.join(logs_dir, 'HEAD')
            if os.path.exists(reflog_file):
                with open(reflog_file, 'r') as f:
                    lines = f.readlines()
                    for line in lines[-20:]:  # Last 20 entries
                        print(line.strip())
        
    except Exception as e:
        print(f"Error reading git directory: {e}")

if __name__ == "__main__":
    check_git_direct()