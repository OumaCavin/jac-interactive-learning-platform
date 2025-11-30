#!/bin/bash
# JAC Platform - Fix Users Health Endpoint 500 Error

echo "=== DIAGNOSING /users/health/ 500 ERROR ==="
echo "Step 1: Check if Django backend containers are running..."
docker-compose ps

echo -e "\nStep 2: Check Django backend logs for specific errors..."
echo "Last 20 lines of backend logs:"
docker-compose logs --tail=20 backend

echo -e "\nStep 3: Test database connectivity..."
docker-compose exec backend python manage.py check --database

echo -e "\nStep 4: Check if users app migrations exist..."
docker-compose exec backend python manage.py showmigrations users

echo -e "\nStep 5: Run migrations for users app..."
docker-compose exec backend python manage.py makemigrations users
docker-compose exec backend python manage.py migrate users

echo -e "\nStep 6: Test the health endpoint directly..."
curl -v http://localhost:8000/users/health/ 2>&1

echo -e "\nStep 7: Check Django admin to confirm backend is working..."
curl -s http://localhost:8000/admin/login/ | grep -o "Django administration" || echo "Admin page not accessible"

echo -e "\n=== DIAGNOSTIC COMPLETE ==="
echo "Check the output above for the specific error causing the 500 response."