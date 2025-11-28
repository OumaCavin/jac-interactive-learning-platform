#!/bin/bash
echo "=== Manual PostgreSQL Fix (In case git push fails) ==="

# Navigate to project
cd ~/projects/jac-interactive-learning-platform

# Backup current settings
cp backend/config/settings.py backend/config/settings.py.backup.$(date +%Y%m%d_%H%M%S)

# Apply the fix directly
echo "Applying PostgreSQL charset fix..."

# Remove the invalid charset option
sed -i '/charset.*utf8/d' backend/config/settings.py

# Also remove empty lines after OPTIONS {
sed -i '/OPTIONS/,/}/{
    /^[[:space:]]*$/d
    /^OPTIONS:/d
    /^[[:space:]]*}/d
}' backend/config/settings.py

# Alternative: Complete replacement of the OPTIONS section
sed -i '109,111c\
        '\''OPTIONS'\'': {\
            # PostgreSQL handles encoding through LC_ settings, not connection options\
        },' backend/config/settings.py

# Verify the fix
echo -e "\nVerifying the fix (should show OPTIONS without charset):"
sed -n '105,115p' backend/config/settings.py

# Test the fix
echo -e "\n4. Testing the fix by rebuilding backend..."
docker-compose up -d --build backend

echo -e "\n5. Waiting 10 seconds for backend to connect..."
sleep 10

echo -e "\n6. Testing database connection:"
docker-compose exec backend python manage.py check --database default

echo -e "\n=== Manual Fix Applied ==="