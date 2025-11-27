# Database Configuration Fix

## Issue: SQLite Read-Only Database Error

The error shows the system is trying to use SQLite instead of PostgreSQL, which suggests a database configuration issue.

## Solutions:

### 1. Check Database Configuration
```bash
# Check current database settings
docker-compose exec backend python manage.py shell -c "
from django.conf import settings;
print('DATABASES:', settings.DATABASES)
"
```

### 2. Fix Database Permissions
```bash
# Check if SQLite database exists and fix permissions
docker-compose exec backend ls -la /app/
docker-compose exec backend ls -la /app/*.sqlite3
docker-compose exec backend chmod 664 /app/*.sqlite3 2>/dev/null || echo "No SQLite files found"
```

### 3. Verify PostgreSQL Connection
```bash
# Test PostgreSQL connection
docker-compose exec postgres psql -U jac_user -d jac_learning_db -c "SELECT 1"
```

### 4. Force PostgreSQL Usage
```bash
# Ensure Django uses PostgreSQL by checking environment
docker-compose exec backend python manage.py check --database
```

### 5. Reset Database and Use PostgreSQL
```bash
# Remove SQLite files and ensure PostgreSQL is used
docker-compose exec backend rm -f /app/db.sqlite3
docker-compose exec backend rm -f /app/*.sqlite3
docker-compose restart backend
```

### 6. Check Docker Environment Variables
```bash
# Verify environment variables are passed correctly
docker-compose exec backend env | grep -E "(DATABASE|POSTGRES|DB_)"
```