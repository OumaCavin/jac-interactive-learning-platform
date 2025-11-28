#!/bin/bash
echo "=== Manual PostgreSQL Charset Fix ==="

# 1. Navigate to your project
cd ~/projects/jac-interactive-learning-platform

# 2. Edit the settings file to remove the charset option
echo "2. Fixing backend/config/settings.py..."

# Show current database config
echo "Current database config (lines 101-114):"
sed -n '101,114p' backend/config/settings.py

# Backup the file
cp backend/config/settings.py backend/config/settings.py.backup

# Create the fix
cat > /tmp/database_fix.txt << 'EOF'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='jac_learning_db'),
        'USER': config('DB_USER', default='jac_user'),
        'PASSWORD': config('DB_PASSWORD', default='jac_password'),
        'HOST': config('DB_HOST', default='postgres'),
        'PORT': config('DB_PORT', default='5432'),
        'OPTIONS': {
            # PostgreSQL handles encoding through LC_ settings, not connection options
        },
        'CONN_MAX_AGE': 60,
    }
}
EOF

# Apply the fix by replacing lines 101-114
sed -i '101,114c\
DATABASES = {\
    '\''default'\'': {\
        '\''ENGINE'\'': '\''django.db.backends.postgresql'\'',\
        '\''NAME'\'': config('\''DB_NAME'\'', default='\''jac_learning_db'\''),\
        '\''USER'\'': config('\''DB_USER'\'', default='\''jac_user'\''),\
        '\''PASSWORD'\'': config('\''DB_PASSWORD'\'', default='\''jac_password'\''),\
        '\''HOST'\'': config('\''DB_HOST'\'', default='\''postgres'\''),\
        '\''PORT'\'': config('\''DB_PORT'\'', default='\''5432'\''),\
        '\''OPTIONS'\'': {\
            # PostgreSQL handles encoding through LC_ settings, not connection options\
        },\
        '\''CONN_MAX_AGE'\'': 60,\
    }\
}' backend/config/settings.py

echo -e "\nFixed database config:"
sed -n '101,114p' backend/config/settings.py

# 3. Test the fix
echo -e "\n3. Testing the fix..."

# Rebuild backend
docker-compose up -d --build backend

echo -e "\n4. Waiting for backend to start..."
sleep 10

echo -e "\n5. Testing database connection:"
docker-compose exec backend python manage.py check --database default

echo -e "\n6. Running migrations:"
docker-compose exec backend python manage.py migrate

echo -e "\n=== Fix Complete ==="