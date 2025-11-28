#!/bin/bash

# Comprehensive cleanup to replace Cavin Otieno with Cavin Otieno
# and prepare for professional commits

set -e

echo "=== JAC Interactive Learning Platform - Professional Cleanup ==="
echo ""

# Configure git properly
echo "Configuring git user as OumaCavin..."
git config user.name "OumaCavin"
git config user.email "cavin.otieno012@gmail.com"
git branch -M main

echo ""
echo "=== Searching for Cavin Otieno references ==="

# Find all files containing Cavin Otieno (case insensitive)
MINIMAX_FILES=$(grep -ril "Cavin Otieno" . 2>/dev/null || true)

if [ -n "$MINIMAX_FILES" ]; then
    echo "Found files with Cavin Otieno references:"
    echo "$MINIMAX_FILES"
    echo ""
    
    # Replace Cavin Otieno with Cavin Otieno in all files
    echo "Replacing Cavin Otieno → Cavin Otieno..."
    find . -type f \( -name "*.py" -o -name "*.js" -o -name "*.jsx" -o -name "*.ts" -o -name "*.tsx" -o -name "*.md" -o -name "*.txt" -o -name "*.sh" -o -name "*.yml" -o -name "*.yaml" \) -exec sed -i 's/Cavin Otieno/Cavin Otieno/gI' {} \;
    
    echo "✅ All Cavin Otieno references replaced with Cavin Otieno"
else
    echo "✅ No Cavin Otieno references found"
fi

echo ""
echo "=== Replacing 'MiniMax' with 'Cavin Otieno' in appropriate contexts ==="

# Replace MiniMax with Cavin Otieno in author contexts
find . -type f \( -name "*.py" -o -name "*.js" -o -name "*.jsx" -o -name "*.ts" -o -name "*.tsx" -o -name "*.md" -o -name "*.txt" \) -exec sed -i 's/^# Author.*MiniMax/# Author: Cavin Otieno/gI' {} \;
find . -type f \( -name "*.py" -o -name "*.js" -o -name "*.jsx" -o -name "*.ts" -o -name "*.tsx" -o -name "*.md" -o -name "*.txt" \) -exec sed -i 's/^## Author.*MiniMax/## Author: Cavin Otieno/gI' {} \;
find . -type f \( -name "*.py" -o -name "*.js" -o -name "*.jsx" -o -name "*.ts" -o -name "*.tsx" -o -name "*.md" -o -name "*.txt" \) -exec sed -i 's/Created by.*MiniMax/Created by Cavin Otieno/gI' {} \;

echo "✅ Author context replacements completed"

echo ""
echo "=== Professional git operations ==="

# Stage all changes
git add .

# Check if there are changes to commit
if git diff --staged --quiet; then
    echo "No changes to commit"
else
    echo "Committing changes with professional message..."
    
    git commit -m "refactor(authorship): Replace Cavin Otieno references with Cavin Otieno

- Update all author attributions and metadata
- Replace Cavin Otieno → Cavin Otieno in code, docs, and comments
- Ensure consistent authorship across the platform
- Maintain code quality while updating metadata"
    
    echo "✅ Professional commit created"
fi

echo ""
echo "=== Pushing to main branch ==="

# Configure remote with token
git remote set-url origin https://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@github.com/OumaCavin/jac-interactive-learning-platform.git

# Push to main
if git push origin main; then
    echo ""
    echo "🎉 SUCCESS: All changes pushed to GitHub main branch!"
    echo ""
    echo "✅ Completed tasks:"
    echo "   • Configured git user: OumaCavin (cavin.otieno012@gmail.com)"
    echo "   • Enforced main branch"
    echo "   • Replaced Cavin Otieno references with Cavin Otieno"
    echo "   • Created professional commit message"
    echo "   • Pushed to GitHub repository"
    echo ""
    echo "📊 Repository Status:"
    git log --oneline -1
else
    echo ""
    echo "❌ Push failed. Check authentication."
    exit 1
fi