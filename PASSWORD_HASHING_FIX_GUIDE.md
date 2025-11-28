# 🚨 CRITICAL: Password Hashing Issue and Fix

## The Problem

Your database setup script created users with **invalid password hashes**:

```sql
-- WRONG: This is just a placeholder string, not a real hash!
'pbkdf2_sha256$720000$HashedPassword'
```

When you try to login with:
- **Username**: `admin`
- **Password**: `admin123`

**Django will:**
1. Hash the entered password `"admin123"` using pbkdf2_sha256
2. Compare it with the database value `"HashedPassword"`
3. **The comparison will FAIL** ❌

## The Fix

I've created two scripts to fix this critical issue:

### Option 1: Python Fix Script
**File**: `fix_password_hashing.py`

**What it does**:
- Uses Django's `create_user()` method which handles password hashing properly
- Creates admin user with correct hash for password `"admin123"`
- Creates demo user with correct hash for password `"demo123"`
- Verifies that password verification works

### Option 2: Shell Fix Script
**File**: `fix_password_hashing.sh`

**What it does**:
- Runs the Python fix script inside the Docker container
- Provides fallback method using Django shell commands
- Tests password verification for both users
- Shows final verification results

## How to Apply the Fix

### Method 1: Using Docker (Recommended)
```bash
cd ~/projects/jac-interactive-learning-platform

# Copy the fix script to backend container
docker cp /workspace/fix_password_hashing.py backend:/tmp/

# Run the fix script
docker-compose exec backend python /tmp/fix_password_hashing.py
```

### Method 2: Using Shell Script
```bash
cd ~/projects/jac-interactive-learning-platform

# Copy the shell script
docker cp /workspace/fix_password_hashing.sh backend:/tmp/

# Run the fix script
docker-compose exec backend bash /tmp/fix_password_hashing.sh
```

### Method 3: Manual Django Commands
```bash
cd ~/projects/jac-interactive-learning-platform

# Access backend shell
docker-compose exec backend python manage.py shell

# In the Django shell:
from django.contrib.auth.models import User

# Remove bad users
User.objects.filter(username='admin').delete()
User.objects.filter(username='demo_user').delete()

# Create admin with proper hashing
admin_user = User.objects.create_user(
    username='admin',
    email='cavin.otieno012@gmail.com',
    password='admin123'
)
admin_user.is_superuser = True
admin_user.is_staff = True
admin_user.save()

# Create demo user with proper hashing
demo_user = User.objects.create_user(
    username='demo_user',
    email='demo@example.com',
    password='demo123'
)

# Verify it works
print("✅ Admin password check:", admin_user.check_password('admin123'))
print("✅ Demo password check:", demo_user.check_password('demo123'))
```

## What Proper Password Hashing Looks Like

After the fix, your database will contain:

```sql
-- Admin user with REAL hash
username: admin
password: pbkdf2_sha256$720000$abc123def456...real_hash_here...
email: cavin.otieno012@gmail.com
is_superuser: true
is_staff: true

-- Demo user with REAL hash  
username: demo_user
password: pbkdf2_sha256$720000$xyz789ghi012...real_hash_here...
email: demo@example.com
is_superuser: false
is_staff: false
```

The hash format `pbkdf2_sha256$720000$salt$hash` shows:
- **Algorithm**: pbkdf2_sha256
- **Iterations**: 720000
- **Salt**: Random salt value
- **Hash**: Actual hash of the password

## Testing the Fix

After running the fix, test login:

### Django Admin
- URL: http://localhost:8000/admin/
- Username: `admin`
- Password: `admin123`

### Frontend Login
- URL: http://localhost:3000/login
- Username: `demo_user`
- Password: `demo123`

## Verification Commands

```bash
# Check if users exist with proper hashes
docker-compose exec backend python manage.py shell << EOF
from django.contrib.auth.models import User
admin = User.objects.get(username='admin')
demo = User.objects.get(username='demo_user')
print("Admin hash:", admin.password[:50] + "...")
print("Demo hash:", demo.password[:50] + "...")
print("Admin password check:", admin.check_password('admin123'))
print("Demo password check:", demo.check_password('demo123'))
EOF
```

## Why This Happened

The original database setup script used:
```sql
VALUES ('admin', 'email', 'pbkdf2_sha256$720000$HashedPassword', ...)
```

The problem:
- `'HashedPassword'` is just a string literal
- Django expects a properly computed hash
- No salt or actual password hashing was performed
- Login attempts will always fail

## Summary

✅ **Issue Identified**: Database contains placeholder password hashes  
✅ **Fix Available**: Scripts to create users with proper Django hashing  
✅ **Testing**: Verify that password verification works correctly  
✅ **Result**: Login will work with `admin/admin123` and `demo_user/demo123`

**Next Step**: Run one of the fix scripts above to resolve this critical issue.