# JAC Learning Platform - Admin Interface Guide

## Overview
The JAC Learning Platform provides two different administrative interfaces for managing the system:

## 1. Django Admin Interface (`http://localhost:8000/admin`)

### Description
- **Built-in Django admin panel** for backend database management
- Traditional Django interface for managing the entire application
- Provides direct access to the database and system configuration

### Features
- User management (create, edit, delete users)
- Database record management
- Model administration
- System-level configuration
- Permission and group management
- Data import/export capabilities

### Access Requirements
- Django `is_staff=True` in the User model
- Django admin permissions
- Access through the Django backend (port 8000)

### How to Access
1. Visit `http://localhost:8000/admin` in your browser
2. Log in with Django admin credentials
3. Navigate through different database models and tables

---

## 2. React Frontend Admin Dashboard (`http://localhost:3000/admin`)

### Description
- **Custom React-based admin interface** for the learning platform
- Modern, user-friendly dashboard for platform administrators
- Focused on learning platform-specific management tasks

### Features
- **User Analytics & Management**
  - View user statistics and activity
  - Manage user accounts and roles
  - Monitor user engagement and progress

- **Content Management**
  - Create and edit learning paths
  - Manage modules and lessons
  - Content approval workflow

- **Learning Path Administration**
  - Monitor learning path performance
  - Manage course structure
  - Track completion rates

- **System Overview**
  - Platform statistics dashboard
  - Recent activity monitoring
  - Performance metrics

### Access Requirements
- Frontend user with `is_staff: true` flag
- Must be logged in through the React frontend
- Admin route protection (built-in)

---

## Demo Accounts for Testing

### Regular User Account
- **Email:** `demo@example.com`
- **Password:** `demo123`
- **Privileges:** Regular user (no admin access)
- **Can Access:** Learning platform features, but NOT admin dashboard

### Administrator Account
- **Email:** `admin@jac.com`
- **Password:** `admin123`
- **Privileges:** Full admin access
- **Can Access:** All learning platform features + admin dashboard

---

## Route Protection Behavior

### Non-Admin User访问 `/admin`
When a non-admin user tries to access `http://localhost:3000/admin`:

1. **Route Protection Activates**
   - AdminRoute component checks `user.is_staff` flag
   - User is redirected to "Access Denied" page

2. **Access Denied Page Shows**
   - Clear message explaining admin privileges required
   - List of admin features available
   - "Go Back" button to return to previous page

3. **No Dashboard Access**
   - User never sees the admin dashboard interface
   - Proper security boundaries maintained

### Admin User访问 `/admin`
When an admin user accesses `http://localhost:3000/admin`:

1. **Route Protection Passes**
   - AdminRoute confirms `user.is_staff: true`
   - User proceeds to admin dashboard

2. **Full Admin Dashboard**
   - Complete admin interface available
   - All admin features accessible
   - User analytics and management tools

---

## Technical Implementation

### AdminRoute Component
```typescript
// Located: frontend/src/components/auth/AdminRoute.tsx
// Protects admin routes by checking user.is_staff flag
// Provides Access Denied page for non-admin users
```

### Route Configuration
```typescript
// Located: frontend/src/App.tsx
// Admin routes wrapped with AdminRoute component instead of ProtectedRoute
<Route 
  path="/admin" 
  element={
    <AdminRoute>
      <MainLayout>
        <PageTransition pageKey="admin">
          <AdminDashboard />
        </PageTransition>
      </MainLayout>
    </AdminRoute>
  } 
/>
```

### User Authentication
```typescript
// Located: frontend/src/services/authService.ts
// Mock admin user with is_staff: true
{
  id: '2',
  username: 'admin_user',
  email: 'admin@jac.com',
  first_name: 'Admin',
  last_name: 'User',
  is_staff: true, // Key admin privilege flag
  // ... other user properties
}
```

---

## Troubleshooting

### Issue: Non-admin user sees regular dashboard instead of Access Denied
**Solution:** AdminRoute component now properly checks `user.is_staff` flag

### Issue: Admin user can't access admin features
**Solution:** Ensure user has `is_staff: true` in their profile

### Issue: Django Admin vs Frontend Admin confusion
**Solution:** Use the demo accounts provided for testing different privilege levels

---

## Security Features

1. **Route-level Protection:** AdminRoute component prevents unauthorized access
2. **User-level Verification:** Checks `is_staff` flag for all admin operations
3. **Graceful Degradation:** Clear error messages for unauthorized access attempts
4. **Separation of Concerns:** Django backend admin vs Frontend admin clearly separated

---

## Development Notes

### Recent Changes
- Added AdminRoute component for proper route protection
- Implemented admin demo user for testing
- Updated routing to use AdminRoute for `/admin` path
- Removed duplicate admin checks from AdminDashboard component
- Enhanced access denied page with feature descriptions

### Files Modified
- `frontend/src/components/auth/AdminRoute.tsx` (NEW)
- `frontend/src/App.tsx` (Updated routing)
- `frontend/src/services/authService.ts` (Added admin demo user)
- `frontend/src/pages/AdminDashboard.tsx` (Removed duplicate checks)

---

## Usage Examples

### Test Non-Admin Access
1. Login with `demo@example.com` / `demo123`
2. Navigate to `/admin`
3. Should see "Access Denied" page

### Test Admin Access
1. Login with `admin@jac.com` / `admin123`
2. Navigate to `/admin`
3. Should see full admin dashboard

### Compare Admin Interfaces
1. Django Admin: `http://localhost:8000/admin`
2. Frontend Admin: `http://localhost:3000/admin`
3. Note different interfaces and capabilities

---

*Last Updated: 2025-11-23*