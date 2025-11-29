# JAC Platform - Fix User Admin Permissions
# This fixes the admin access denied issue for the custom User model

# ========================================
# METHOD 1: Automated Script (Recommended)
# ========================================

# Copy this script to your project and run:
docker-compose exec backend python /app/fix_user_permissions_final.py


# ========================================
# METHOD 2: Manual Django Shell Commands
# ========================================

# Enter the Django shell:
docker-compose exec backend python manage.py shell

# Then run these commands in the shell:

from apps.users.models import User

# Get the user
user = User.objects.get(username='Ouma')

# Check current permissions
print(f"Username: {user.username}")
print(f"is_superuser: {user.is_superuser}")
print(f"is_staff: {user.is_staff}")
print(f"is_active: {user.is_active}")

# Fix the permissions
user.is_superuser = True
user.is_staff = True
user.is_active = True
user.save()

# Verify the fix
user.refresh_from_db()
print(f"After fix - is_superuser: {user.is_superuser}")
print(f"After fix - is_staff: {user.is_staff}")
print(f"After fix - is_active: {user.is_active}")

print("✅ Admin permissions fixed!")

# Exit shell
exit()


# ========================================
# METHOD 3: Quick One-Liner
# ========================================

# Run this command directly:
docker-compose exec backend python -c "
from apps.users.models import User
user = User.objects.get(username='Ouma')
user.is_superuser = True
user.is_staff = True
user.is_active = True
user.save()
print('✅ Fixed admin permissions for user Ouma')
print(f'is_superuser: {user.is_superuser}')
print(f'is_staff: {user.is_staff}')
print(f'is_active: {user.is_active}')
"