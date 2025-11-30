#!/bin/bash

echo "=========================================="
echo "JAC Platform - Final Migration Setup"
echo "=========================================="
echo ""
echo "✅ Admin user already created successfully"
echo "🔧 Now fixing migration permissions and applying database changes"
echo ""

cd ~/projects/jac-interactive-learning-platform

echo "Step 1: Fixing migration permissions..."
bash DIRECT_PERMISSION_FIX.sh

echo ""
echo "Step 2: Creating migrations (manual fallback)..."
docker-compose exec backend python manage.py makemigrations collaboration gamification jac_execution learning --noinput

echo ""
echo "Step 3: Applying migrations..."
docker-compose exec backend python manage.py migrate

echo ""
echo "Step 4: Verifying setup..."
bash VERIFY_USERS.sh

echo ""
echo "=========================================="
echo "🎯 FINAL VERIFICATION"
echo "=========================================="
echo "📚 Django Admin: http://localhost:8000/admin/"
echo "   Login: admin / jac_admin_2024!"
echo ""
echo "🔗 API Login: http://localhost:8000/api/auth/login/"
echo "💻 Frontend: http://localhost:3000/"
echo ""
echo "✅ Check all containers are healthy:"
echo "   docker-compose ps"
echo ""
echo "🌐 Test the platform!"