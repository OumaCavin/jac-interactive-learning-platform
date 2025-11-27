# Backend Status Check Commands

## Quick Status Overview
```bash
# Check if all containers are running
docker-compose ps

# Check backend logs for PostgreSQL connection
docker-compose logs -f backend
```

## Expected PostgreSQL Connection Messages
Look for these messages in your backend logs:

✅ **Success indicators:**
- "PostgreSQL database connection successful"
- "Applying database migrations..." 
- "Watching for file changes with StatReloader"

❌ **Error indicators:**
- "OperationalError: connection to server"
- "django.db.utils.OperationalError"

## Database Health Check
```bash
# Test database connection specifically
docker-compose exec backend python manage.py check --database default

# If successful, you should see: "System check identified no issues (0 silenced)."
```

## Create Admin User
Once backend connects to PostgreSQL successfully:
```bash
docker-compose exec backend python manage.py createsuperuser
```

**Login Credentials:**
- URL: http://localhost:8000/admin/
- Username: admin
- Password: admin123

## Troubleshooting Steps

### If Backend Won't Start
```bash
# Pull the latest changes we made
git pull origin main

# Rebuild and restart
docker-compose down
docker-compose up -d --build
```

### If PostgreSQL Connection Fails
```bash
# Check if PostgreSQL container is running
docker-compose logs postgres

# Check environment variables
docker-compose exec backend python -c "import os; print('DB_PASSWORD:', os.getenv('DB_PASSWORD'))"
```