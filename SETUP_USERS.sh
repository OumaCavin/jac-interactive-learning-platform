#!/bin/bash

# JAC Interactive Learning Platform - User Setup Script
# Creates superuser, admin users, and test users for the learning platform

echo "=========================================="
echo "JAC Interactive Learning Platform"
echo "User Setup - Superuser & Test Users"
echo "=========================================="

cd ~/projects/jac-interactive-learning-platform

# First, ensure migrations are applied
echo ""
echo "📊 Checking migration status..."
docker-compose exec backend python manage.py showmigrations | grep -E "collaboration|gamification|jac_execution|learning" | grep -v "\[X\]" || echo "✅ All migrations applied"

echo ""
echo "👤 CREATING USERS FOR JAC PLATFORM"
echo "=================================="

# Create Superuser
echo ""
echo "🔑 Creating Superuser..."
echo "Using custom createsuperuser command..."

# Create admin superuser
docker-compose exec backend python manage.py createsuperuser \
    --username admin \
    --email admin@jacplatform.com \
    --password jac_admin_2024! \
    --noinput

echo ""
echo "👨‍💼 Creating Admin User (instructor role)..."
docker-compose exec backend python manage.py createsuperuser \
    --username instructor \
    --email instructor@jacplatform.com \
    --password jac_instructor_2024! \
    --noinput

echo ""
echo "👩‍🎓 Creating Student User..."
docker-compose exec backend python manage.py createsuperuser \
    --username student1 \
    --email student1@jacplatform.com \
    --password jac_student_2024! \
    --noinput

echo ""
echo "👨‍🎓 Creating Student User 2..."
docker-compose exec backend python manage.py createsuperuser \
    --username student2 \
    --email student2@jacplatform.com \
    --password jac_student_2024! \
    --noinput

echo ""
echo "✅ USER SETUP COMPLETED!"
echo ""
echo "👤 CREATED USERS:"
echo "================="
echo "🔑 Admin Superuser:"
echo "   Username: admin"
echo "   Email: admin@jacplatform.com"
echo "   Password: jac_admin_2024!"
echo "   Role: Superuser, Staff, Admin"
echo ""
echo "👨‍💼 Instructor:"
echo "   Username: instructor"
echo "   Email: instructor@jacplatform.com"
echo "   Password: jac_instructor_2024!"
echo "   Role: Superuser, Staff, Instructor"
echo ""
echo "👩‍🎓 Students:"
echo "   Username: student1"
echo "   Email: student1@jacplatform.com"
echo "   Password: jac_student_2024!"
echo ""
echo "   Username: student2"
echo "   Email: student2@jacplatform.com"
echo "   Password: jac_student_2024!"
echo ""

echo ""
echo "🌐 ACCESS POINTS:"
echo "================"
echo "📚 Django Admin: http://localhost:8000/admin/"
echo "   Use admin credentials above"
echo ""
echo "🔗 API Endpoints: http://localhost:8000/api/"
echo "   Use any user credentials for authentication"
echo ""
echo "💻 Frontend: http://localhost:3000/"
echo ""

echo ""
echo "🎉 SUCCESS! Your JAC Interactive Learning Platform now has users!"
echo "You can now test authentication, API endpoints, and all platform features."
