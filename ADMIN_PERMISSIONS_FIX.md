# JAC Platform - Admin Permissions Fix

This fix resolves the admin access denied issue by providing custom management commands and signal handlers.

## Problem Fixed

The issue was that Django's default `createsuperuser` command doesn't properly set admin permissions (`is_superuser`, `is_staff`) for custom User models. Users created through `createsuperuser` could not access the Django admin interface.

## Solution Components

### 1. Custom `createsuperuser` Command
**File**: `apps/users/management/commands/createsuperuser.py`

- Properly sets `is_superuser`, `is_staff`, and `is_active` flags
- Handles the custom User model from `apps.users.models.User`
- Includes comprehensive validation and error handling

### 2. Fix User Permissions Command  
**File**: `apps/users/management/commands/fix_user_permissions.py`

- Can fix permissions for individual users or all users
- Useful for fixing users created before the custom command was implemented
- Command line options:
  - `--username`: Fix specific user
  - `--all`: Fix all users
  - `--make-superuser`: Make user a superuser

### 3. Signal Handler
**File**: `apps/users/signals.py`

- Ensures admin permissions are maintained automatically
- Automatically sets `is_staff` and `is_active` when `is_superuser` is True

## Usage Instructions

### Creating a New Superuser
```bash
# Interactive mode (recommended)
docker-compose exec backend python manage.py createsuperuser

# Non-interactive mode
docker-compose exec backend python manage.py createsuperuser --username=admin --email=admin@example.com --password=securepassword --noinput
```

### Fixing Existing Users
```bash
# Fix a specific user
docker-compose exec backend python manage.py fix_user_permissions --username=Ouma --make-superuser

# Fix all users
docker-compose exec backend python manage.py fix_user_permissions --all

# Make a specific user superuser
docker-compose exec backend python manage.py fix_user_permissions --username=admin --make-superuser
```

### Using the Standard Django Command
The standard Django createsuperuser command should now work correctly with the signal handler:

```bash
docker-compose exec backend python manage.py createsuperuser
```

## Automatic Fix

After deploying these changes, any user created as a superuser will automatically have the correct admin permissions thanks to the signal handler.

## Testing the Fix

1. Create a new superuser or fix existing user permissions
2. Clear browser cache/cookies for localhost:8000
3. Go to http://localhost:8000/admin/
4. Login with your superuser credentials
5. You should now have full admin access

## Files Modified

- `apps/users/management/commands/createsuperuser.py` (NEW)
- `apps/users/management/commands/fix_user_permissions.py` (NEW)
- `apps/users/management/__init__.py` (NEW)
- `apps/users/management/commands/__init__.py` (NEW)
- `apps/users/signals.py` (MODIFIED - added signal handler)

## Benefits

1. **Reliable Superuser Creation**: The custom command ensures proper permissions
2. **Fix Existing Issues**: The fix command can repair broken admin access
3. **Automatic Maintenance**: Signal handler prevents future permission issues
4. **Better Error Messages**: More informative feedback during user creation
5. **Validation**: Proper password and input validation

This fix ensures that the JAC Platform admin interface is always accessible to superusers.