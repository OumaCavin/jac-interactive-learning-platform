#!/bin/bash

# JAC Interactive Learning Platform - Verify User Setup
# Checks if users were created successfully and shows user details

echo "=========================================="
echo "JAC Interactive Learning Platform"
echo "User Setup Verification"
echo "=========================================="

cd ~/projects/jac-interactive-learning-platform

echo ""
echo "🔍 Verifying user setup in database..."

# Check total users
echo ""
echo "📊 Total users in database:"
docker-compose exec backend python manage.py shell -c "
from apps.users.models import User
print(f'Total users: {User.objects.count()}')
"

echo ""
echo "👤 Listing all users:"
docker-compose exec backend python manage.py shell -c "
from apps.users.models import User
users = User.objects.all().order_by('username')
for user in users:
    print(f'  {user.username:<15} | {user.email:<25} | Superuser: {user.is_superuser} | Staff: {user.is_staff} | Active: {user.is_active}')
"

echo ""
echo "🔑 Superusers:"
docker-compose exec backend python manage.py shell -c "
from apps.users.models import User
superusers = User.objects.filter(is_superuser=True)
print(f'Superuser count: {superusers.count()}')
for user in superusers:
    print(f'  {user.username} ({user.email})')
"

echo ""
echo "👨‍💼 Staff users:"
docker-compose exec backend python manage.py shell -c "
from apps.users.models import User
staff = User.objects.filter(is_staff=True)
print(f'Staff count: {staff.count()}')
for user in staff:
    print(f'  {user.username} ({user.email})')
"

echo ""
echo "🧪 Test API Authentication:"
echo "=========================="

echo ""
echo "🔗 Testing login with admin user..."
curl -s -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "jac_admin_2024!"}' | head -10 || echo "Login test - API endpoint may need exact path"

echo ""
echo "🌐 ACCESS INFORMATION:"
echo "====================="
echo "📚 Django Admin: http://localhost:8000/admin/"
echo "   Superuser: admin / jac_admin_2024!"
echo ""
echo "🔗 API Login: http://localhost:8000/api/auth/login/"
echo "   Use any created username/password"
echo ""
echo "💻 Frontend: http://localhost:3000/"

echo ""
echo "✅ User verification completed!"
