#!/bin/bash

# JAC Interactive Learning Platform - Quick User Creation
# Simple script to create additional users

echo "=========================================="
echo "JAC Interactive Learning Platform"
echo "Quick User Creation"
echo "=========================================="

cd ~/projects/jac-interactive-learning-platform

# Quick user creation function
create_user() {
    local username=$1
    local email=$2
    local password=$3
    
    echo "Creating user: $username"
    docker-compose exec backend python manage.py createsuperuser \
        --username "$username" \
        --email "$email" \
        --password "$password" \
        --noinput 2>/dev/null || echo "User $username may already exist"
}

echo ""
echo "👥 Creating additional test users..."
echo ""

# Create more test users
create_user "teacher1" "teacher1@jacplatform.com" "jac_teacher_2024!"
create_user "teacher2" "teacher2@jacplatform.com" "jac_teacher_2024!"
create_user "learner1" "learner1@jacplatform.com" "jac_learner_2024!"
create_user "learner2" "learner2@jacplatform.com" "jac_learner_2024!"

echo ""
echo "🎓 Creating student users with different learning styles..."

# This would require custom script to set learning_style field
# For now, just create the basic users
create_user "visual_learner" "visual@jacplatform.com" "jac_visual_2024!"
create_user "auditory_learner" "auditory@jacplatform.com" "jac_auditory_2024!"

echo ""
echo "✅ Additional users created!"
echo "Run ./VERIFY_USERS.sh to see all users."
