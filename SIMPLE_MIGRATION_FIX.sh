#!/bin/bash
# Alternative Simple Fix - Run this from your project root
echo "Fixing permissions and completing migrations..."

# Fix permissions inside container
docker-compose exec backend bash -c "
    chmod -R 755 /app/apps/*/migrations/
    find /app/apps -name '*.py' -path '*/migrations/*' -exec chmod 644 {} \;
"

# Try migration again with less verbose output
docker-compose exec backend python manage.py makemigrations collaboration gamification jac_execution learning --noinput || echo "Manual migration may be needed"

# Apply migrations
docker-compose exec backend python manage.py migrate

echo "✅ Migration process completed!"