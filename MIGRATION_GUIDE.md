# JAC Learning Platform - Migration & Deployment Guide

## Overview
The JAC Learning Platform now includes automatic migration handling and superadmin functionality. This document explains how database migrations work and how to set up the platform.

## Migration Handling

### Automatic Migration (Recommended)
The platform now automatically handles migrations when the Docker containers start up:

```bash
# Start the platform
docker-compose up -d

# The backend will automatically:
# 1. Wait for the database to be ready
# 2. Run database migrations
# 3. Create a superuser account
# 4. Start the Django server
```

### Manual Migration (Alternative)
If you prefer to run migrations manually:

```bash
# Run migrations
docker-compose exec backend python manage.py migrate

# Create superuser (if not auto-created)
docker-compose exec backend python manage.py createsuperuser

# Or use the initialization command
docker-compose exec backend python manage.py initialize_platform --username=admin --email=admin@jacplatform.com --password=admin123
```

## Superadmin Access

### Default Superadmin Credentials
- **Username:** `admin`
- **Email:** `admin@jacplatform.com`
- **Password:** `admin123`

### Custom Superadmin Creation
You can create a custom superuser with the management command:

```bash
# Custom admin creation
docker-compose exec backend python manage.py initialize_platform \
  --username=your_admin \
  --email=your_admin@email.com \
  --password=your_secure_password
```

### Admin Dashboard Access
Once logged in as an admin user, you can access the admin dashboard at:
- **URL:** `http://localhost:3000/admin`
- **Features:**
  - User management
  - Learning path management
  - Content creation and editing
  - Platform analytics
  - Assessment management

### Django Admin Interface
You can also access the Django admin interface at:
- **URL:** `http://localhost:8000/admin/`
- **Purpose:** Direct database management and advanced configuration

## Platform Features for Superadmin

### 1. User Management
- View all registered users
- Manage user roles and permissions
- Track user activity and progress
- Suspend/activate user accounts

### 2. Content Management
- Create and edit learning paths
- Add modules and lessons
- Upload media resources
- Manage course prerequisites

### 3. Assessment Management
- Create assessments and quizzes
- Define question banks
- Set scoring rules
- Monitor completion rates

### 4. Platform Analytics
- User engagement metrics
- Learning path performance
- Completion rates
- Time spent tracking

### 5. System Configuration
- Platform settings
- Agent configuration
- Email notifications
- Integration management

## File Structure

```
backend/
├── apps/
│   ├── management/
│   │   └── commands/
│   │       └── initialize_platform.py  # Migration & setup command
│   ├── learning/
│   │   └── admin.py                    # Admin interface for content
│   └── users/
│       └── admin.py                    # User management interface
└── Dockerfile                          # Auto-migration setup
```

## Environment Variables

Ensure these environment variables are set in your `.env` file:

```bash
# Database
DB_NAME=jac_learning_db
DB_USER=jac_user
DB_PASSWORD=your_secure_password

# Django
SECRET_KEY=your_django_secret_key
DEBUG=False

# Email (for notifications)
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
```

## Migration Process Flow

1. **Container Startup**: Backend container starts
2. **Database Check**: Waits for PostgreSQL to be ready
3. **Migration Check**: Checks for pending migrations
4. **Migrations Run**: Executes `makemigrations` and `migrate`
5. **Superuser Creation**: Creates admin account if it doesn't exist
6. **Server Start**: Django server starts on port 8000

## Troubleshooting

### Migration Issues
```bash
# Check migration status
docker-compose exec backend python manage.py showmigrations

# Reset migrations (development only)
docker-compose exec backend python manage.py migrate apps.users zero
docker-compose exec backend python manage.py migrate

# Create fresh migrations
docker-compose exec backend python manage.py makemigrations
docker-compose exec backend python manage.py migrate
```

### Permission Issues
```bash
# Check file permissions
docker-compose exec backend ls -la /app

# Fix ownership
docker-compose exec backend chown -R jac:jac /app
```

### Database Connection Issues
```bash
# Check database status
docker-compose exec postgres pg_isready -U jac_user

# View database logs
docker-compose logs postgres
```

## Production Deployment

### Environment Setup
```bash
# Set production environment
export DEBUG=False
export ENVIRONMENT=production

# Use secure passwords and keys
export SECRET_KEY=your_production_secret_key
export DB_PASSWORD=your_production_db_password
```

### Database Backup
```bash
# Create backup
docker-compose exec postgres pg_dump -U jac_user jac_learning_db > backup.sql

# Restore backup
docker-compose exec -T postgres psql -U jac_user jac_learning_db < backup.sql
```

### SSL/HTTPS Setup
Update nginx configuration for SSL certificates in production.

## Security Considerations

1. **Change Default Credentials**: Always change the default admin password
2. **Secure Secret Key**: Use a strong Django secret key in production
3. **Database Security**: Use strong database passwords
4. **Environment Variables**: Keep sensitive data in environment variables
5. **HTTPS**: Always use HTTPS in production
6. **Regular Updates**: Keep Docker images and dependencies updated

## Support

For issues or questions:
1. Check the logs: `docker-compose logs`
2. Verify database connectivity
3. Check environment variables
4. Review Django admin interface for configuration issues
