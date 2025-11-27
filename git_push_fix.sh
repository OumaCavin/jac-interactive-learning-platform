#!/bin/bash
echo "=== Pushing PostgreSQL Charset Fix ==="

# Navigate to backend directory
cd ~/projects/jac-interactive-learning-platform

# Check if there are changes to push
echo "1. Checking git status..."
git status

# Set up authentication with token
echo -e "\n2. Setting up authentication..."

# Use your existing PAT (Personal Access Token)
GITHUB_PAT="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"
REPO_URL="https://github.com/OumaCavin/jac-interactive-learning-platform.git"

# Push using token authentication
echo "3. Pushing changes..."
git push https://$GITHUB_PAT@$REPO_URL main

echo -e "\n=== Push Complete ==="