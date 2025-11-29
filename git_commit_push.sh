#!/bin/bash
# Script to commit and push admin fixes to GitHub

echo "=== Starting Git Operations ==="

# Navigate to the project directory
cd /workspace/jac-interactive-learning-platform

echo "Current directory: $(pwd)"

# Check git status
echo "=== Git Status ==="
git status

# Add all files
echo "=== Adding all files ==="
git add .

# Commit with descriptive message
echo "=== Committing changes ==="
git commit -m "fix(admin): resolve admin access issue with custom admin site

- Fixed all admin.py files to properly register models with custom_admin_site
- Added missing imports: from config.custom_admin import custom_admin_site
- Updated all @admin.register decorators to include site=custom_admin_site parameter
- Resolved SyntaxError: keyword argument repeated: site in decorators
- Cleaned up duplicate import statements across 9 admin.py files
- Ensures proper admin access at /admin/ without Access Denied errors"

# Check if commit was successful
if [ $? -eq 0 ]; then
    echo "=== Commit successful ==="
    
    # Push to GitHub
    echo "=== Pushing to GitHub ==="
    git push origin main
    
    if [ $? -eq 0 ]; then
        echo "=== SUCCESS: Changes pushed to GitHub ==="
    else
        echo "=== ERROR: Push failed ==="
    fi
else
    echo "=== ERROR: Commit failed ==="
fi