#!/bin/bash
# Clean up commit history - Run these commands one by one

echo "=== EXECUTING CLEANUP COMMANDS ==="
echo

# Check current status
echo "1. Checking current status..."
git status
echo

# Show what commits will be combined
echo "2. Showing commits to be combined:"
git log --oneline d587cb1..HEAD | head -5
echo

# Perform the cleanup
echo "3. Performing soft reset to combine commits..."
git reset --soft d587cb1
echo

echo "4. Committing with clean message..."
git commit -m "feat: Complete Django migration conflict resolution

Fix all Django migration conflicts and eliminate interactive prompts:

Learning App:
- Fix UserDifficultyProfile field conflicts (last_assessment → last_difficulty_change)
- Add generation_prompt field to AdaptiveChallenge model  
- Add generated_by_agent field to track AI agent generation
- Add timing fields to UserChallengeAttempt model

Database Schema Improvements:
- Add unique constraints across collaboration models
- Add performance indexes for better query performance
- Add missing tracking fields to Badge and Achievement models
- Add missing status tracking fields to CodeExecution model
- Add missing interactive element fields to ContentBlock

Migration Operations:
- Explicit RenameField, AddField, and AlterField operations
- Nullable fields for existing row compatibility
- All 8 migration files with proper dependencies

This resolves all interactive migration prompts and ensures
clean database schema matching model definitions."
echo

echo "5. Showing new clean commit:"
git log --oneline -1
echo

echo "=== READY TO PUSH ==="
echo "Execute: git push --force-with-lease origin main"