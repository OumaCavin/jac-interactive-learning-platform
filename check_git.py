import subprocess
import os

os.chdir('/workspace')

# Direct git operations without shell=True
try:
    # Check if we're in a git repository
    print("Checking git repository status...")
    
    # Check status
    result = subprocess.run(['git', 'status'], capture_output=True, text=True, timeout=30)
    print("Git status result:")
    print("Return code:", result.returncode)
    print("Output:", result.stdout)
    if result.stderr:
        print("Error:", result.stderr)
    
    # Add changes
    print("\nAdding changes...")
    result = subprocess.run(['git', 'add', '.'], capture_output=True, text=True, timeout=30)
    print("Add result:", result.returncode)
    if result.stdout:
        print("Add output:", result.stdout)
    
    # Check status again
    print("\nChecking status after add...")
    result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True, timeout=30)
    print("Status after add:", result.stdout)
    
    if result.stdout.strip():
        # Commit
        print("\nCommitting changes...")
        commit_msg = "Fix: Enhanced migration automation across all setup scripts"
        result = subprocess.run(['git', 'commit', '-m', commit_msg], capture_output=True, text=True, timeout=30)
        print("Commit result:", result.returncode)
        if result.stdout:
            print("Commit output:", result.stdout)
        if result.stderr:
            print("Commit error:", result.stderr)
            
        # Push
        print("\nPushing changes...")
        result = subprocess.run(['git', 'push', 'origin', 'main'], capture_output=True, text=True, timeout=60)
        print("Push result:", result.returncode)
        if result.stdout:
            print("Push output:", result.stdout)
        if result.stderr:
            print("Push error:", result.stderr)
    else:
        print("No changes to commit")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()