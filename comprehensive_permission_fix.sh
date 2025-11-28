#!/bin/bash

echo "🔧 Running comprehensive permission fix for Django migrations..."

# Fix permissions for all migration directories
echo "→ Fixing permissions for all migration directories..."

# Find and fix permissions for all migrations directories
docker-compose exec -T backend bash -c "
cd /app
find . -type d -name migrations -exec chmod -R 755 {} \; 2>/dev/null || true
find . -type d -name migrations -exec ls -la {} \; 2>/dev/null || true
echo 'Migration directories permissions:'
find . -type d -name migrations -exec ls -ld {} \; 2>/dev/null || true
" || echo "Migration permission fix attempted"

echo "✅ Permission fix completed"