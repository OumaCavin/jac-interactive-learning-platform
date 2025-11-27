#!/bin/bash
# Clean commit history by combining recent messy commits into one clean commit

echo "=== CLEANING UP COMMIT HISTORY ==="
echo

# Find the last meaningful commit before the system-generated ones
LAST_GOOD_COMMIT="d587cb1"  # "Merge remote changes with migration fixes"

echo "Found last good commit: $LAST_GOOD_COMMIT"
echo

echo "Step 1: Soft reset to combine all recent commits"
echo "git reset --soft $LAST_GOOD_COMMIT"
echo

echo "Step 2: Create clean commit message"
echo "git commit -m \"feat: Complete Django migration conflict resolution

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
clean database schema matching model definitions.\""
echo

echo "Step 3: Force push to clean history"
echo "git push --force-with-lease origin main"
echo

echo "=== EXECUTE THESE COMMANDS IN YOUR TERMINAL ==="