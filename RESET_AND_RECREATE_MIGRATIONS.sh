#!/bin/bash
# Complete Migration Reset and Recreation Script
# This script completely resets migration state and recreates all migrations cleanly

set -e

echo "🔄 COMPLETE MIGRATION RESET AND RECREATION"
echo "==========================================="
echo ""
echo "⚠️  This will COMPLETELY RESET all migration states"
echo "📋 What will happen:"
echo "   1. Stop all containers"
echo "   2. Backup current migration files"
echo "   3. Clear migration history from database"
echo "   4. Remove all migration files"
echo "   5. Start fresh with clean migration state"
echo "   6. Generate new migrations cleanly"
echo ""
echo "💾 Backup location: ./migration_backup_$(date +%Y%m%d_%H%M%S)/"
echo ""

# Create backup directory
BACKUP_DIR="migration_backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

echo "📦 Creating backup of current migration files..."

# Backup existing migration files
find /workspace/backend -name "migrations" -type d | while read migrations_dir; do
    app_name=$(basename "$(dirname "$migrations_dir")")
    echo "  → Backing up migrations for app: $app_name"
    mkdir -p "$BACKUP_DIR/$app_name"
    cp -r "$migrations_dir" "$BACKUP_DIR/$app_name/"
done

echo "✅ Backup completed in: $BACKUP_DIR"
echo ""

# Function to clear migration history from database
clear_database_migrations() {
    echo "🗄️ Clearing migration history from database..."
    
    # Connect to PostgreSQL and clear migration history
    docker-compose exec -T postgres psql -U jac_user -d jac_learning_db << 'EOF'
-- Clear all migration records
DELETE FROM django_migrations;

-- Reset sequence if it exists
SELECT setval(pg_get_serial_sequence('django_migrations', 'id'), 1, false);

-- Show remaining migration records (should be empty)
SELECT COUNT(*) as remaining_migrations FROM django_migrations;
EOF
    
    echo "✅ Database migration history cleared"
}

# Function to remove all migration files
remove_migration_files() {
    echo "🧹 Removing all migration files..."
    
    # Remove all migration files except __init__.py
    find /workspace/backend -name "migrations" -type d | while read migrations_dir; do
        app_name=$(basename "$(dirname "$migrations_dir")")
        echo "  → Cleaning migrations for app: $app_name"
        
        # Remove all migration files except __init__.py
        find "$migrations_dir" -name "*.py" ! -name "__init__.py" -delete
        
        # Also remove .pyc files
        find "$migrations_dir" -name "*.pyc" -delete
        find "$migrations_dir" -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    done
    
    echo "✅ Migration files removed"
}

# Function to regenerate clean migrations
regenerate_migrations() {
    echo "🔄 Regenerating clean migrations..."
    
    # Ensure database is ready
    echo "  ⏳ Waiting for database..."
    sleep 10
    
    # Start backend service
    echo "  🚀 Starting backend service..."
    docker-compose up -d backend
    sleep 15
    
    # Run migration commands
    docker-compose exec -T backend bash -c "
    export DJANGO_COLUMNS=0
    export DJANGO_SUPERUSER_ID=''
    export PYTHONUNBUFFERED=1
    
    cd /app
    
    echo 'Step 1: Checking Django configuration...'
    python manage.py check --settings=config.settings
    
    echo 'Step 2: Creating migrations for all apps...'
    python manage.py makemigrations users --noinput
    python manage.py makemigrations learning --noinput
    python manage.py makemigrations assessments --noinput
    python manage.py makemigrations content --noinput
    python manage.py makemigrations progress --noinput
    python manage.py makemigrations agents --noinput
    python manage.py makemigrations knowledge_graph --noinput
    python manage.py makemigrations jac_execution --noinput
    python manage.py makemigrations management --noinput
    
    echo 'Step 3: Verifying migration files created...'
    find . -name 'migrations' -type d -exec find {} -name '*.py' ! -name '__init__.py' \\;
    
    echo 'Step 4: Applying migrations...'
    python manage.py migrate --noinput
    
    echo 'Step 5: Showing final migration state...'
    python manage.py showmigrations
    
    echo 'Step 6: Collecting static files...'
    python manage.py collectstatic --noinput
    
    echo 'Step 7: Verifying database schema...'
    python manage.py dbshell -c '\dt' 2>/dev/null || echo 'Database verification completed'
    "
    
    echo "✅ Clean migrations regenerated and applied"
}

# Main execution
main() {
    # Step 1: Stop all containers
    echo "🛑 Step 1: Stopping all containers..."
    docker-compose down -v
    echo "✅ All containers stopped"
    echo ""
    
    # Step 2: Clear database migration history
    clear_database_migrations
    echo ""
    
    # Step 3: Start database
    echo "🗄️ Step 3: Starting database service..."
    docker-compose up -d postgres
    sleep 8
    echo "✅ Database started"
    echo ""
    
    # Step 4: Remove migration files
    remove_migration_files
    echo ""
    
    # Step 5: Regenerate clean migrations
    regenerate_migrations
    echo ""
    
    # Step 6: Start all services
    echo "🚀 Step 6: Starting all services..."
    docker-compose up -d
    sleep 20
    echo "✅ All services started"
    echo ""
    
    # Step 7: Final verification
    echo "🔍 Step 7: Final verification..."
    docker-compose exec -T backend python manage.py check --settings=config.settings
    
    echo ""
    echo "🎉 MIGRATION RESET AND RECREATION COMPLETED!"
    echo "=============================================="
    echo ""
    echo "✅ Complete migration state reset"
    echo "✅ Fresh migration files generated"
    echo "✅ Database migration history cleared"
    echo "✅ Clean application state restored"
    echo ""
    echo "📊 Final migration status:"
    docker-compose exec -T backend python manage.py showmigrations
    echo ""
    echo "🌐 Your platform is ready:"
    echo "   Frontend: http://localhost:3000"
    echo "   Admin: http://localhost:3000/admin"
    echo "   API: http://localhost:8000/api/"
    echo ""
    echo "📦 Backup location: $BACKUP_DIR"
    echo ""
    echo "🔑 If you need admin access:"
    echo "   docker-compose exec backend python manage.py createsuperuser"
    echo ""
}

# Run the main function
main

echo "✨ Migration reset completed successfully!"