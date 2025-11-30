#!/bin/bash

echo "🔧 Quick Admin Permission Fix"
echo "==============================="

cd ~/projects/jac-interactive-learning-platform

# Fix admin user permissions
docker-compose exec backend python manage.py shell -c "
from apps.users.models import User
admin = User.objects.get(username='admin')
admin.is_superuser = True
admin.is_staff = True
admin.is_active = True
admin.save()
print('✅ Admin permissions fixed')
print(f'Superuser: {admin.is_superuser}')
print(f'Staff: {admin.is_staff}')
print(f'Active: {admin.is_active}')
"

# Restart backend
docker-compose restart backend

echo ""
echo "✅ Admin fix complete! Try logging in again:"
echo "🌐 http://localhost:8000/admin/"
echo "👤 admin / jac_admin_2024!"