#!/bin/bash

echo "🛠️  Emergency Migration Fix for JAC Platform"
echo "=========================================="

# Navigate to project directory (adjust path as needed)
cd ~/projects/jac-interactive-learning-platform

echo "🚨 EMERGENCY FIX: Resetting broken migrations..."

# Step 1: Stop services
echo "🛑 Step 1: Stopping services..."
docker-compose down

# Step 2: Clean everything
echo "🗑️  Step 2: Complete cleanup (WARNING: Deletes ALL data)..."
docker-compose down -v

# Step 3: Remove problematic migration files
echo "🧹 Step 3: Cleaning migration files..."
rm -f backend/apps/content/migrations/0003_fix_missing_fields.py
rm -f backend/apps/gamification/migrations/0002_fix_missing_fields.py  
rm -f backend/apps/jac_execution/migrations/0003_fix_missing_fields.py
rm -f backend/apps/learning/migrations/0004_user_difficulty_profile_field_fixes.py
rm -f backend/apps/learning/migrations/0005_add_generation_prompt.py
rm -f backend/apps/learning/migrations/0006_add_missing_fields.py
rm -f backend/apps/learning/migrations/0007_add_generated_by_agent_field.py

# Step 4: Fix migration directory permissions
echo "🔧 Step 4: Fixing permissions..."
find backend/apps/*/migrations -type d -exec chmod 755 {} \;
find backend/apps/*/migrations -type f -exec chmod 644 {} \;

# Step 5: Rebuild and start
echo "🏗️  Step 5: Rebuilding containers..."
docker-compose up -d --build

echo "⏳ Step 6: Waiting for services (45 seconds)..."
sleep 45

# Step 7: Clear any existing migration state
echo "🧹 Step 7: Clearing migration cache..."
docker-compose exec -T backend python manage.py migrate --fake-initial --noinput || true
docker-compose exec -T backend rm -rf apps/*/migrations/__pycache__/ || true

# Step 8: Apply basic migrations only
echo "📊 Step 8: Applying core migrations..."
docker-compose exec -T backend python manage.py migrate content 0002 --noinput || true
docker-compose exec -T backend python manage.py migrate gamification 0001 --noinput || true
docker-compose exec -T backend python manage.py migrate jac_execution 0002 --noinput || true
docker-compose exec -T backend python manage.py migrate learning 0003 --noinput || true

# Step 9: Apply all migrations
echo "🔄 Step 9: Applying all migrations..."
docker-compose exec -T backend python manage.py migrate --noinput

# Step 10: Create admin user
echo "👤 Step 10: Creating admin user..."
docker-compose exec -T backend python manage.py shell << 'EOF'
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()
try:
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'cavin.otieno012@gmail.com', 'admin123')
        print("✅ Admin user created successfully")
    else:
        print("✅ Admin user already exists")
except Exception as e:
    print(f"❌ Error: {e}")
EOF

# Step 11: Final verification
echo "✅ Step 11: Final verification..."
docker-compose exec -T backend python manage.py showmigrations

echo ""
echo "🎉 EMERGENCY FIX COMPLETED!"
echo "=========================="
echo ""
echo "🌐 Services should now be working:"
echo "  • Admin:  http://localhost:8000/admin/"
echo "  • Login:  http://localhost:3000/login"
echo ""
echo "🔑 Credentials:"
echo "  • admin / admin123"
echo ""
echo "📋 If still having issues, check:"
echo "  docker-compose logs backend"