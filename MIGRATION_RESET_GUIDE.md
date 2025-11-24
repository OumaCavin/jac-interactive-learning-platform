# 🔄 Complete Migration Reset and Recreation Guide

## 📋 **Overview**

This guide explains how to completely reset Django migration state and recreate migrations cleanly to resolve migration prompts and conflicts.

## 🎯 **When to Use This Guide**

Use this guide when you encounter:
- ❌ Django migration prompts asking about field changes
- ❌ "Table already exists" errors
- ❌ Migration conflicts between branches
- ❌ Corrupted migration state
- ❌ Foreign key constraint errors
- ❌ Database schema inconsistencies

## 🔧 **Migration Reset Strategy**

### **What the Reset Does:**
1. **Stops all services** - Ensures clean state
2. **Backs up current migrations** - Preserves existing work
3. **Clears database migration history** - Removes Django's migration records
4. **Removes migration files** - Deletes all `.py` files except `__init__.py`
5. **Regenerates clean migrations** - Creates fresh migration files
6. **Applies migrations cleanly** - Establishes correct database state

### **Why This Works:**
- **Fresh Start**: Removes all migration conflicts and inconsistencies
- **Clean Generation**: Django creates new migrations based on current model state
- **Database Reset**: Clears migration history to avoid conflicts
- **Backup Protection**: Original migrations are preserved for reference

## 🚀 **Quick Reset (Recommended)**

Run the automated script:
```bash
chmod +x RESET_AND_RECREATE_MIGRATIONS.sh
./RESET_AND_RECREATE_MIGRATIONS.sh
```

This script will:
- ✅ Complete backup of current migrations
- ✅ Reset database migration history
- ✅ Clean all migration files
- ✅ Regenerate fresh migrations
- ✅ Apply migrations automatically
- ✅ Start all services
- ✅ Verify the setup

## 📝 **Manual Reset Steps**

If you prefer manual control or the script doesn't work:

### **Step 1: Stop All Services**
```bash
# Stop all containers
docker-compose down -v

# Remove any cached Docker images (optional)
docker system prune -f --volumes
```

### **Step 2: Clear Database Migration History**
```bash
# Start database
docker-compose up -d postgres
sleep 8

# Connect to database and clear migration history
docker-compose exec -T postgres psql -U jac_user -d jac_learning_db << 'EOF'
DELETE FROM django_migrations;
SELECT setval(pg_get_serial_sequence('django_migrations', 'id'), 1, false);
SELECT COUNT(*) FROM django_migrations;
EOF
```

### **Step 3: Remove Migration Files**
```bash
# Remove all migration files except __init__.py
find /workspace/backend -name "migrations" -type d | while read migrations_dir; do
    echo "Cleaning: $migrations_dir"
    find "$migrations_dir" -name "*.py" ! -name "__init__.py" -delete
    find "$migrations_dir" -name "*.pyc" -delete
    find "$migrations_dir" -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
done
```

### **Step 4: Generate Fresh Migrations**
```bash
# Start backend
docker-compose up -d backend
sleep 15

# Generate migrations for each app
docker-compose exec -T backend bash -c "
cd /app

# Check Django configuration
python manage.py check --settings=config.settings

# Create migrations for all apps
python manage.py makemigrations users --noinput
python manage.py makemigrations learning --noinput
python manage.py makemigrations assessments --noinput
python manage.py makemigrations content --noinput
python manage.py makemigrations progress --noinput
python manage.py makemigrations agents --noinput
python manage.py makemigrations knowledge_graph --noinput
python manage.py makemigrations jac_execution --noinput
python manage.py makemigrations management --noinput

# Apply migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput
"
```

### **Step 5: Verify and Start Services**
```bash
# Check migration state
docker-compose exec -T backend python manage.py showmigrations

# Start all services
docker-compose up -d

# Verify Django setup
docker-compose exec -T backend python manage.py check --settings=config.settings
```

## 🔍 **Verification Steps**

After reset, verify everything works:

### **1. Check Migration State**
```bash
docker-compose exec backend python manage.py showmigrations
```
Expected output:
```
users
 [X] 0001_initial
 [X] 0002_auto_...
learning
 [X] 0001_initial
 [X] 0002_add_missing_models
...
```

### **2. Verify Database Schema**
```bash
docker-compose exec backend python manage.py dbshell -c '\dt'
```
Should show tables like:
- auth_user
- jac_learning_path
- jac_assessment_attempts
- etc.

### **3. Test Django Configuration**
```bash
docker-compose exec backend python manage.py check --settings=config.settings
```
Should output:
```
System check identified no issues (0 silenced).
```

### **4. Test API Endpoints**
```bash
curl http://localhost:8000/api/health/
```
Should return HTTP 200 with health status.

## 🛡️ **Backup and Recovery**

### **Automatic Backup**
The automated script automatically creates backups:
```
migration_backup_YYYYMMDD_HHMMSS/
├── users/migrations/...
├── learning/migrations/...
└── assessments/migrations/...
```

### **Manual Backup**
Before any reset, manually backup:
```bash
# Create backup directory
mkdir -p migration_backup_manual

# Copy all migration files
cp -r backend/*/migrations migration_backup_manual/
```

### **Recovery Process**
To restore from backup:
```bash
# Stop services
docker-compose down -v

# Restore migration files
cp -r migration_backup_manual/* backend/*/migrations/

# Clear database migration history
docker-compose up -d postgres
sleep 8
docker-compose exec -T postgres psql -U jac_user -d jac_learning_db << 'EOF'
DELETE FROM django_migrations;
SELECT setval(pg_get_serial_sequence('django_migrations', 'id'), 1, false);
EOF

# Continue with regular migration process
docker-compose up -d backend
docker-compose exec -T backend python manage.py migrate --noinput
```

## 🔧 **Troubleshooting**

### **Common Issues and Solutions**

#### **1. "relation already exists" Error**
**Problem**: Database tables already exist but migration records are missing.
**Solution**: Use `--fake-initial` flag:
```bash
python manage.py migrate --fake-initial --noinput
```

#### **2. "column X does not exist" Error**
**Problem**: Application code expects column that migration didn't create.
**Solution**: Reset migrations and regenerate:
```bash
# Follow complete reset process above
```

#### **3. "circular dependency detected" Error**
**Problem**: Models have circular foreign key relationships.
**Solution**: Manually fix models or use `--empty` flag:
```bash
python manage.py makemigrations app_name --empty --noinput
```

#### **4. Permission Denied Errors**
**Problem**: Docker container can't write to filesystem.
**Solution**: Fix volume permissions:
```bash
sudo chown -R $(whoami):$(whoami) backend/
chmod -R 755 backend/
```

### **Emergency Recovery**
If everything fails:
```bash
# Nuclear option - full reset
docker-compose down -v --remove-orphans
docker system prune -af --volumes
docker volume prune -f

# Rebuild everything
docker-compose up -d --build
```

## 📊 **Migration Best Practices**

### **Development Workflow**
1. **Make model changes** in Django models
2. **Generate migrations**: `python manage.py makemigrations`
3. **Review migration files** before applying
4. **Apply migrations**: `python manage.py migrate`
5. **Commit migrations** to version control

### **Production Deployment**
1. **Test migrations** on staging environment first
2. **Create backups** before applying migrations
3. **Use transactions** for critical migrations
4. **Monitor application** after migration deployment

### **Code Review Guidelines**
- Review all generated migration files
- Ensure migrations are reversible
- Check for data loss potential
- Validate foreign key relationships

## 🎉 **Success Indicators**

After successful reset, you should see:
- ✅ No migration prompts or errors
- ✅ All migration records applied
- ✅ Database schema matches models
- ✅ Application starts without errors
- ✅ API endpoints respond correctly
- ✅ Admin interface accessible

## 📞 **Support**

If issues persist:
1. Check Docker logs: `docker-compose logs backend`
2. Review Django logs: `docker-compose logs -f backend`
3. Verify database connection: `docker-compose exec postgres pg_isready -U jac_user`
4. Test Django shell: `docker-compose exec backend python manage.py shell`

---

**Remember**: The migration reset is a powerful tool but should be used carefully in production environments. Always create backups and test thoroughly before applying to critical systems.