#!/bin/bash
# JAC Interactive Learning Platform - Correct Permission Fix Inside Container
# Author: MiniMax Agent
# Created: 2025-11-30

echo "🔧 Fixing Permissions INSIDE Docker Container"
echo "=============================================="

echo "Option 1: Fix permissions INSIDE the container..."
docker-compose exec backend bash -c "
    # Change to the app directory
    cd /app
    
    # Fix ownership if needed (if jac user exists)
    if id 'jac' &>/dev/null; then
        chown -R jac:jac apps/*/migrations/
    fi
    
    # Fix permissions on all migration files
    chmod -R 755 apps/*/migrations/
    find apps -name '*.py' -path '*/migrations/*' -exec chmod 644 {} \;
    
    # List permissions to verify
    ls -la apps/*/migrations/ | head -10
"

echo ""
echo "Option 2: Alternative - Run makemigrations as root temporarily..."
docker-compose exec --user root backend bash -c "
    cd /app
    chmod -R 755 apps/*/migrations/
    find apps -name '*.py' -path '*/migrations/*' -exec chmod 644 {} \;
    # Exit root user
    exit
"

echo ""
echo "Option 3: Check if volume is mounted to host..."
docker-compose exec backend bash -c "
    # Check if we're in a volume mount
    mount | grep '/app'
    
    # Check current user and permissions
    whoami
    ls -la apps/*/migrations/ | head -5
"