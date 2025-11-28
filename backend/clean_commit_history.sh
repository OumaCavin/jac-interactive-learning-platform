#!/bin/bash
# Script to clean up commit history and rewrite with meaningful messages
# This script will help you replace system-generated commit messages

echo "=== Git Commit History Cleanup Script ==="
echo
echo "This script will help you rewrite commit messages to be more meaningful."
echo
echo "Current problematic commits found:"
git log --oneline -10 | grep "Message [0-9]"
echo
echo "=== RECOMMENDED APPROACH: Interactive Rebase ==="
echo
echo "Step 1: Find the commit before the problematic ones"
echo "git log --oneline | grep -v 'Message [0-9]' | tail -1"
echo
echo "Step 2: Start interactive rebase"
echo "git rebase -i <commit-hash-from-step-1>"
echo
echo "Step 3: In the editor, change 'pick' to 'reword' for commits with bad messages"
echo
echo "Step 4: Replace each system message with meaningful commit messages like:"
echo
echo "For migration fixes:"
echo "feat: Fix Django migration conflicts across learning app"
echo "feat: Add missing database constraints and indexes"
echo "feat: Add generation_prompt and generated_by_agent fields"
echo "feat: Add timing fields to UserChallengeAttempt model"
echo "feat: Add interactive element fields to ContentBlock"
echo "feat: Add status tracking fields to CodeExecution model"
echo
echo "=== ALTERNATIVE: Quick Fix ==="
echo "If you want to quickly combine all recent commits into one clean commit:"
echo "git reset --soft $(git log --oneline | grep -v 'Message [0-9]' | tail -1 | cut -d' ' -f1)"
echo "git commit -m \"feat: Complete Django migration conflict resolution

- Fix UserDifficultyProfile field conflicts and renames
- Add missing generation_prompt and generated_by_agent fields  
- Add timing fields to UserChallengeAttempt model
- Add missing database constraints and indexes
- Resolve all interactive migration prompts
- Add missing interactive element fields
- Add status tracking fields for code execution

All migration conflicts resolved with explicit operations.\""
echo
echo "=== AFTER CLEANUP ==="
echo "git push --force-with-lease origin main"
echo
echo "This will create a clean, readable commit history!"