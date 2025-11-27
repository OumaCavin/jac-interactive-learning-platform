# Admin Login Troubleshooting

## Issue: "Please enter the correct username and password for a staff account"

This error means the admin user exists but lacks proper permissions (`is_staff=True` or `is_superuser=True`).

## Solutions:

### 1. Check User Permissions (Inside Container)
```bash
# Check if admin user exists and has correct permissions
docker-compose exec backend python manage.py shell -c "
from django.contrib.auth.models import User;
admin = User.objects.filter(username='admin').first();
if admin:
    print(f'Username: {admin.username}');
    print(f'Email: {admin.email}');
    print(f'Is Staff: {admin.is_staff}');
    print(f'Is Superuser: {admin.is_superuser}');
    print(f'Is Active: {admin.is_active}');
else:
    print('Admin user not found')
"
```

### 2. Fix Admin User Permissions
```bash
# If user exists but lacks permissions
docker-compose exec backend python manage.py shell -c "
from django.contrib.auth.models import User;
admin = User.objects.filter(username='admin').first();
if admin:
    admin.is_staff = True;
    admin.is_superuser = True;
    admin.is_active = True;
    admin.set_password('admin123');
    admin.save();
    print('✅ Admin user permissions updated');
else:
    print('Admin user not found')
"
```

### 3. Create New Admin User (If Above Fails)
```bash
# Delete existing admin and create new one
docker-compose exec backend python manage.py shell -c "
from django.contrib.auth.models import User;
User.objects.filter(username='admin').delete();
admin = User.objects.create_superuser(
    username='admin',
    email='cavin.otieno012@gmail.com',
    password='admin123'
);
admin.is_staff = True;
admin.is_superuser = True;
admin.save();
print('✅ New admin user created successfully')
"
```

### 4. Alternative Admin Creation Method
```bash
# Use Django management command
docker-compose exec backend python manage.py createsuperuser
# Then follow the prompts to set username, email, password
```

### 5. Verify Database Connection
```bash
# Check if database is properly initialized
docker-compose exec backend python manage.py migrate
```

### 6. Check Environment Variables
```bash
# Ensure database and environment are properly configured
docker-compose exec backend python manage.py check
```

## Most Likely Solution:
Run the permission fix command (#2) as this is the most common issue.