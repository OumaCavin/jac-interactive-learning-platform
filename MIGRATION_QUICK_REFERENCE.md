# 🚀 Django Migration Quick Reference

## 🎯 **Common Migration Commands**

### **View Migration Status**
```bash
# Show all migration states
docker-compose exec backend python manage.py showmigrations

# Show migration status for specific app
docker-compose exec backend python manage.py showmigrations learning

# Check for unmigrated changes
docker-compose exec backend python manage.py makemigrations --dry-run
```

### **Generate Migrations**
```bash
# Create migrations for specific app
docker-compose exec backend python manage.py makemigrations learning

# Create migrations for all apps
docker-compose exec backend python manage.py makemigrations

# Create empty migration (for manual SQL)
docker-compose exec backend python manage.py makemigrations app_name --empty

# Create migration without prompts
docker-compose exec backend python manage.py makemigrations --noinput
```

### **Apply Migrations**
```bash
# Apply all pending migrations
docker-compose exec backend python manage.py migrate

# Apply migration for specific app
docker-compose exec backend python manage.py migrate learning

# Apply migrations without prompts
docker-compose exec backend python manage.py migrate --noinput

# Apply migrations as "fake" (mark as applied without running SQL)
docker-compose exec backend python manage.py migrate --fake

# Apply fake-initial migrations (for existing tables)
docker-compose exec backend python manage.py migrate --fake-initial
```

### **Reset Migrations (Nuclear Option)**
```bash
# Remove all migration files except __init__.py
find backend/*/migrations -name "*.py" ! -name "__init__.py" -delete

# Clear database migration history
docker-compose exec -T postgres psql -U jac_user -d jac_learning_db -c "DELETE FROM django_migrations;"

# Regenerate migrations from current models
docker-compose exec backend python manage.py makemigrations --noinput
docker-compose exec backend python manage.py migrate --noinput
```

## 🛠️ **Migration Management Tasks**

### **1. Resolve "Field Rename" Prompts**
```bash
# When Django asks about renaming fields
# Choose option 2: "Provide a one-off default now"
# Then specify the default value or migration will be created

# Alternative: Use --noinput to avoid prompts
docker-compose exec backend python manage.py makemigrations --noinput
```

### **2. Handle "Table Already Exists" Errors**
```bash
# For existing tables without migration records
docker-compose exec backend python manage.py migrate --fake-initial

# For inconsistent migration state
docker-compose exec backend python manage.py migrate --fake app_name
```

### **3. Fix Migration Conflicts**
```bash
# Remove conflicted migration files
rm backend/apps/learning/migrations/0002_conflicted_migration.py

# Reset migration state for that app
docker-compose exec backend python manage.py migrate app_name zero
docker-compose exec backend python manage.py makemigrations app_name
docker-compose exec backend python manage.py migrate app_name
```

### **4. Add Fields to Existing Models**
```bash
# Django will prompt for default values for existing rows
# Choose option 1: "Provide a one-off default now"
# Then specify appropriate default value
```

### **5. Remove Models/Fields**
```bash
# Django handles deletions automatically
docker-compose exec backend python manage.py makemigrations --noinput
```

## 📊 **Migration Troubleshooting**

### **Common Error Patterns**

#### **"relation already exists"**
```bash
# Solution: Use fake-initial
docker-compose exec backend python manage.py migrate --fake-initial
```

#### **"column does not exist"**
```bash
# Solution: Reset migrations completely
# See MIGRATION_RESET_GUIDE.md for full reset procedure
```

#### **"circular dependency detected"**
```bash
# Solution: Create empty migration and add dependencies manually
docker-compose exec backend python manage.py makemigrations app_name --empty
# Then edit the migration file to fix dependencies
```

#### **"ValueError: Related model cannot be resolved"**
```bash
# Solution: Check model imports and foreign key relationships
# Ensure all models are properly imported and defined
```

### **Migration Recovery Commands**
```bash
# Reset specific app migrations
docker-compose exec backend python manage.py migrate app_name zero

# Rollback to specific migration
docker-compose exec backend python manage.py migrate app_name 0001

# Show SQL that would be executed
docker-compose exec backend python manage.py sqlmigrate app_name 0001
```

## 🔍 **Diagnostic Commands**

### **Migration Status Check**
```bash
# Comprehensive migration status
docker-compose exec backend python manage.py showmigrations

# Check for unmigrated model changes
docker-compose exec backend python manage.py makemigrations --dry-run

# Show migration plan
docker-compose exec backend python manage.py migrate --plan
```

### **Database Inspection**
```bash
# List all tables
docker-compose exec backend python manage.py dbshell -c "\dt"

# Show table structure
docker-compose exec backend python manage.py dbshell -c "\d table_name"

# Show migration records
docker-compose exec -T postgres psql -U jac_user -d jac_learning_db -c "SELECT * FROM django_migrations;"
```

### **Model Validation**
```bash
# Check for model issues
docker-compose exec backend python manage.py check --deploy

# Validate model relationships
docker-compose exec backend python manage.py check --settings=config.settings
```

## 📝 **Migration Best Practices**

### **Development Workflow**
1. **Make model changes**
2. **Generate migrations**: `makemigrations`
3. **Review migration files**
4. **Apply migrations**: `migrate`
5. **Test thoroughly**

### **Production Deployment**
1. **Test migrations on staging**
2. **Create database backup**
3. **Review migration files for data loss**
4. **Apply migrations during maintenance window**
5. **Monitor application after deployment**

### **Code Review Checklist**
- [ ] Review all generated migration files
- [ ] Ensure migrations are reversible
- [ ] Check for data loss potential
- [ ] Validate foreign key relationships
- [ ] Confirm proper default values
- [ ] Test on staging environment

## 🎯 **Quick Solutions**

| Issue | Command |
|-------|---------|
| Migration prompts | `makemigrations --noinput` |
| Table exists error | `migrate --fake-initial` |
| Field rename prompts | Choose "Provide one-off default" |
| Migration conflicts | Reset specific app: `migrate app_name zero` |
| Circular dependencies | `makemigrations app_name --empty` |
| Complete reset needed | See MIGRATION_RESET_GUIDE.md |

## 📞 **Emergency Commands**

### **Nuclear Reset (Last Resort)**
```bash
# Complete database and migration reset
docker-compose down -v --remove-orphans
docker system prune -af --volumes
docker-compose up -d --build

# Then run migration reset script
./RESET_AND_RECREATE_MIGRATIONS.sh
```

### **Quick Health Check**
```bash
# Verify everything is working
python verify_migration_reset.py

# Or manual checks:
docker-compose exec backend python manage.py check --settings=config.settings
docker-compose exec backend python manage.py showmigrations
curl -s http://localhost:8000/api/health/ | head -1
```

---

**💡 Tip**: Always backup your database before running migration resets in production!