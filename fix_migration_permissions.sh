#!/bin/bash
# Migration Permission Fix Script
# This script resolves common Django migration permission and prompt issues

echo "🔧 JAC Learning Platform - Migration Permission Fix"
echo "================================================="

# Fix permissions for all migration directories
echo "Step 1: Fixing permissions on all migration directories..."
docker-compose exec -T backend bash -c "
cd /app
find . -type d -name migrations -exec chmod -R 755 {} \; 2>/dev/null || true
chmod -R 755 migrations/ 2>/dev/null || true
chmod -R 755 */migrations/ 2>/dev/null || true
echo 'Permissions fixed successfully!'
" || echo "⚠️  Permission fix completed with warnings"

# Handle Django migration prompts automatically
echo "Step 2: Running migrations with automated prompt handling..."
docker-compose exec -T backend bash -c "
cd /app
export DJANGO_COLUMNS=0

# Try standard migration first
echo 'Attempting standard migration...'
python manage.py makemigrations --noinput || {
    echo 'Standard migration had issues, trying with permission fixes...'
    find . -type d -name migrations -exec chmod -R 755 {} \; 2>/dev/null || true
    python manage.py makemigrations --noinput || {
        echo 'Migration requires manual intervention'
        echo 'Common fixes:'
        echo '  - For field rename prompts: type \"y\"'
        echo '  - For default value prompts: type \"1\" then \"\"\"'
        echo '  - For permission errors: the script will fix them'
    }
}

# Apply migrations
python manage.py migrate --noinput || {
    echo 'Migration failed, trying with permission fixes...'
    find . -type d -name migrations -exec chmod -R 755 {} \; 2>/dev/null || true
    python manage.py migrate || echo 'Manual migration may be needed'
}
" || echo "⚠️  Migration completed with warnings"

echo "Step 3: Verifying migration status..."
docker-compose exec -T backend python manage.py showmigrations | tail -5

echo ""
echo "✅ Migration fix process completed!"
echo ""
echo "💡 If you still see prompts:"
echo "  1. For field renames: type 'y'"
echo "  2. For default values: type '1' then '\"\"'"
echo "  3. For permission errors: This script should have fixed them"
echo ""
echo "🔧 Quick commands:"
echo "  • Manual migration: docker-compose exec backend python manage.py migrate"
echo "  • Check status: docker-compose exec backend python manage.py showmigrations"
echo "  • View logs: docker-compose logs -f backend"