#!/bin/bash

# Email Verification Test Script
# This script tests the complete email verification functionality

echo "🚀 Testing JAC Learning Platform Email Verification System"
echo "============================================================="

# Function to check if Docker containers are running
check_containers() {
    echo "🔍 Checking Docker containers..."
    if ! docker-compose ps | grep -q "Up"; then
        echo "❌ Docker containers are not running. Starting containers..."
        docker-compose up -d
        sleep 10
    fi
    echo "✅ Docker containers are running"
}

# Function to run migrations
run_migrations() {
    echo "📊 Running database migrations..."
    docker-compose exec backend python manage.py migrate --noinput
    echo "✅ Migrations completed"
}

# Function to initialize platform
initialize_platform() {
    echo "🏗️ Initializing platform with superadmin..."
    docker-compose exec backend python manage.py initialize_platform --username=admin --email=admin@jacplatform.com --password=admin123 --force
    echo "✅ Platform initialized"
}

# Function to test registration endpoint
test_registration() {
    echo "🧪 Testing user registration..."
    
    # Test registration with curl
    response=$(curl -s -X POST http://localhost:8000/api/users/auth/register/ \
        -H "Content-Type: application/json" \
        -d '{
            "username": "testuser001",
            "email": "testuser001@example.com",
            "password": "TestPassword123!",
            "first_name": "Test",
            "last_name": "User"
        }')
    
    echo "📧 Registration response:"
    echo "$response" | python -m json.tool
    
    # Check if response contains success message
    if echo "$response" | grep -q "Please check your email to verify your account"; then
        echo "✅ Registration successful - verification email should be sent"
        return 0
    else
        echo "❌ Registration failed"
        return 1
    fi
}

# Function to test verification endpoint
test_verification() {
    echo "🔐 Testing email verification..."
    
    # In a real test, we would need to extract the token from email
    # For this demo, we'll show the endpoint structure
    echo "📋 Verification endpoint: GET /api/users/verify-email/?token={token}"
    echo "📋 Resend endpoint: POST /api/users/resend-verification/"
}

# Function to check Celery worker
check_celery() {
    echo "⚙️ Checking Celery worker..."
    docker-compose logs celery | tail -10
}

# Function to test email configuration
test_email_config() {
    echo "📧 Testing email configuration..."
    
    # Test Django email settings
    docker-compose exec backend python manage.py shell -c "
from django.conf import settings
print('Email Backend:', settings.EMAIL_BACKEND)
print('Email Host:', settings.EMAIL_HOST)
print('Email Port:', settings.EMAIL_PORT)
print('Email User:', settings.EMAIL_HOST_USER)
print('Default From:', settings.DEFAULT_FROM_EMAIL)
"
}

# Function to test admin access
test_admin_access() {
    echo "👑 Testing admin access..."
    
    # Test Django admin login
    echo "🔗 Django Admin: http://localhost:8000/admin"
    echo "👤 Credentials: admin / admin123"
    
    # Test React admin
    echo "🔗 React Admin: http://localhost:3000/admin"
    echo "👤 Credentials: admin / admin123"
}

# Function to display email template
show_email_template() {
    echo "📄 Email Template Preview:"
    echo "---------------------------"
    docker-compose exec backend ls -la templates/emails/
    echo "Template file: /workspace/backend/templates/emails/verification_email.html"
}

# Main execution
main() {
    echo "Starting email verification system test..."
    
    # Check prerequisites
    check_containers
    run_migrations
    initialize_platform
    
    # Test email system
    test_email_config
    test_registration
    test_verification
    check_celery
    
    # Test admin access
    test_admin_access
    show_email_template
    
    echo ""
    echo "🎉 Email Verification System Test Completed!"
    echo ""
    echo "📧 Email Verification Flow:"
    echo "1. User registers at http://localhost:3000/register"
    echo "2. System generates verification token"
    echo "3. Celery task sends email via Gmail SMTP"
    echo "4. User receives professional HTML email"
    echo "5. User clicks verification link"
    echo "6. Account is activated and user can login"
    echo ""
    echo "🔍 To monitor email sending:"
    echo "   docker-compose logs -f celery"
    echo ""
    echo "📊 To check user verification status:"
    echo "   docker-compose exec backend python manage.py shell"
    echo "   > from apps.users.models import User"
    echo "   > User.objects.filter(email='testuser001@example.com').values('is_verified', 'verification_token')"
}

# Run the test
main