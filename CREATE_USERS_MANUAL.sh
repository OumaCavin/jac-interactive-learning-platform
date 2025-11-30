#!/bin/bash

# JAC Interactive Learning Platform - Manual User Creation
# This script helps create users one by one with proper error handling

echo "=========================================="
echo "JAC Interactive Learning Platform"
echo "Manual User Creation"
echo "=========================================="

cd ~/projects/jac-interactive-learning-platform

echo ""
echo "⚠️  IMPORTANT: This script requires manual password input"
echo "The custom createsuperuser command does not support --password flag"
echo ""

create_user_interactive() {
    local username=$1
    local email=$2
    local role=$3
    
    echo ""
    echo "================================================="
    echo "Creating $role User"
    echo "================================================="
    echo "Username: $username"
    echo "Email: $email"
    echo ""
    echo "You will be prompted for a password twice."
    echo "Suggested password: jac_${role}_2024!"
    echo ""
    
    # Run the command interactively
    docker-compose exec backend python manage.py createsuperuser \
        --username "$username" \
        --email "$email" || echo "❌ Failed to create user $username"
}

echo "Choose which users to create:"
echo "1. All users (admin, instructor, student1, student2)"
echo "2. Admin only"
echo "3. Admin + Instructor"
echo "4. Custom selection"
echo ""
read -p "Enter your choice (1-4): " choice

case $choice in
    1)
        create_user_interactive "admin" "admin@jacplatform.com" "admin"
        create_user_interactive "instructor" "instructor@jacplatform.com" "instructor"
        create_user_interactive "student1" "student1@jacplatform.com" "student"
        create_user_interactive "student2" "student2@jacplatform.com" "student"
        ;;
    2)
        create_user_interactive "admin" "admin@jacplatform.com" "admin"
        ;;
    3)
        create_user_interactive "admin" "admin@jacplatform.com" "admin"
        create_user_interactive "instructor" "instructor@jacplatform.com" "instructor"
        ;;
    4)
        echo "Enter username:"
        read username
        echo "Enter email:"
        read email
        echo "Enter role:"
        read role
        create_user_interactive "$username" "$email" "$role"
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "✅ User creation process completed!"
echo ""
echo "🔍 Run VERIFY_USERS.sh to check if users were created successfully"
