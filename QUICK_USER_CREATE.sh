#!/bin/bash

# JAC Interactive Learning Platform - Quick User Creation
# Simple script to create users interactively

echo "=========================================="
echo "JAC Interactive Learning Platform"
echo "Quick User Creation"
echo "=========================================="

cd ~/projects/jac-interactive-learning-platform

echo ""
echo "🔑 Creating Admin Superuser..."
echo "Please enter password when prompted:"
docker-compose exec backend python manage.py createsuperuser --username admin --email admin@jacplatform.com

echo ""
echo "✅ Admin user creation completed!"
echo ""
echo "Run ./VERIFY_USERS.sh to verify the user was created"
