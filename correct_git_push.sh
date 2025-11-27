#!/bin/bash
echo "=== Correct Git Push with Valid PAT ==="

cd ~/projects/jac-interactive-learning-platform

# Check current status
echo "1. Checking current git status..."
git status

# Method 1: Push with PAT as username (correct format)
echo -e "\n2. Pushing with PAT as username..."
git push https://OumaCavin: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@github.com/OumaCavin/jac-interactive-learning-platform.git main

# If method 1 succeeds, we're done
if [ $? -eq 0 ]; then
    echo "✅ Push successful!"
    echo "3. Verifying remote was updated..."
    git fetch origin
    git status
else
    echo "❌ Method 1 failed, trying Method 2..."
    
    # Method 2: Set remote URL and push
    echo "Setting remote URL with PAT..."
    git remote set-url origin https://OumaCavin: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@github.com/OumaCavin/jac-interactive-learning-platform.git
    git push origin main
fi

echo -e "\n=== Git Push Attempt Complete ==="