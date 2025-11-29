# Environment Variables Configuration Guide

## Overview
This guide documents the comprehensive environment variable setup for the JAC Learning Platform, replacing all hardcoded values with configurable environment variables.

## ✅ What Was Already Environment-Aware
The following files already had proper environment variable support:

### Frontend Services
- **`frontend/src/services/apiClient.ts`** - Uses `process.env.REACT_APP_API_URL`
- **`frontend/src/services/authService.ts`** - Uses `process.env.REACT_APP_API_URL`
- **`frontend/src/services/websocketService.ts`** - Uses `window.location` (better approach)

### Backend Settings
- **`backend/config/settings.py`** - Extensive use of `config()` from python-decouple
- **`backend/config/settings_minimal.py`** - Environment variable configuration

## 🔧 New Environment Variables Added

### URL Configuration
```bash
# Backend Configuration
BACKEND_HOST=localhost
BACKEND_PORT=8000
USE_HTTPS=false

# Frontend Configuration  
FRONTEND_HOST=localhost
FRONTEND_PORT=3000

# API Configuration (Frontend)
REACT_APP_API_URL=http://localhost:8000

# Test Configuration
TEST_API_URL=http://localhost:8000
```

### CORS Configuration
```bash
# CORS Origins (comma-separated)
CORS_ALLOWED_ORIGINS=http://localhost:3000,https://your-domain.com
```

## 📝 Files Updated

### Backend Management Commands

#### `backend/apps/management/commands/initialize_platform.py`
**Before:**
```python
self.stdout.write(
    self.style.SUCCESS(f'Admin URL: http://localhost:8000/admin/')
)
self.stdout.write(
    self.style.SUCCESS(f'API URL: http://localhost:8000/api/')
)
```

**After:**
```python
# Get environment variables for URLs
import os
backend_host = os.environ.get('BACKEND_HOST', 'localhost')
backend_port = os.environ.get('BACKEND_PORT', '8000')
protocol = 'https' if os.environ.get('USE_HTTPS', 'false').lower() == 'true' else 'http'

admin_url = f"{protocol}://{backend_host}:{backend_port}/admin/"
api_url = f"{protocol}://{backend_host}:{backend_port}/api/"

self.stdout.write(
    self.style.SUCCESS(f'Admin URL: {admin_url}')
)
self.stdout.write(
    self.style.SUCCESS(f'API URL: {api_url}')
)
```

#### `backend/apps/learning/management/commands/populate_jac_curriculum.py`
**Before:**
```python
'  Or use Django admin at http://localhost:8000/admin/'
print("See: http://localhost:8000/admin/ or http://localhost:3000/register");
```

**After:**
```python
# Get environment variables for URLs
import os
backend_host = os.environ.get('BACKEND_HOST', 'localhost')
backend_port = os.environ.get('BACKEND_PORT', '8000')
frontend_host = os.environ.get('FRONTEND_HOST', 'localhost')
frontend_port = os.environ.get('FRONTEND_PORT', '3000')
protocol = 'https' if os.environ.get('USE_HTTPS', 'false').lower() == 'true' else 'http'

backend_url = f"{protocol}://{backend_host}:{backend_port}"
frontend_url = f"{protocol}://{frontend_host}:{frontend_port}"

f'  Or use Django admin at {backend_url}/admin/'
print(f"See: {backend_url}/admin/ or {frontend_url}/register");
```

### Backend Settings

#### `backend/config/settings.py` & `backend/config/settings_minimal.py`
**Before:**
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
```

**After:**
```python
CORS_ALLOWED_ORIGINS = config(
    'CORS_ALLOWED_ORIGINS', 
    default='http://localhost:3000,http://127.0.0.1:3000',
    cast=lambda v: [s.strip() for s in v.split(',')]
)
```

### Frontend Configuration

#### `frontend/src/setupProxy.js` (NEW FILE)
Created a development proxy configuration that respects environment variables:

```javascript
const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
  // Get API URL from environment variable or use default
  const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000';
  
  // Proxy API requests to backend
  app.use(
    '/api',
    createProxyMiddleware({
      target: apiUrl,
      changeOrigin: true,
      pathRewrite: {
        '^/api': '/api', // keep /api in the path
      },
    })
  );

  // Proxy WebSocket connections
  app.use(
    '/ws',
    createProxyMiddleware({
      target: apiUrl.replace('http', 'ws'),
      changeOrigin: true,
      ws: true,
      pathRewrite: {
        '^/ws': '/ws', // keep /ws in the path
      },
    })
  );
};
```

### Test Files

#### `backend/test_predictive_analytics.py`
**Before:**
```python
base_url = "http://localhost:8000"
print("4. Check API endpoints at http://localhost:8000/api/v1/predict/")
```

**After:**
```python
base_url = os.environ.get('TEST_API_URL', 'http://localhost:8000')
print(f"4. Check API endpoints at {base_url}/api/v1/predict/")
```

### Documentation

#### `backend/docs/REAL_TIME_MONITORING_GUIDE.md`
**Before:**
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/dashboard/');
```

**After:**
```javascript
const ws = new WebSocket(`ws://${window.location.host}/ws/dashboard/`);
```

## 🚀 Usage Examples

### Development Environment
```bash
# .env file
BACKEND_HOST=localhost
BACKEND_PORT=8000
FRONTEND_HOST=localhost
FRONTEND_PORT=3000
REACT_APP_API_URL=http://localhost:8000
USE_HTTPS=false
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### Production Environment (HTTP)
```bash
# .env file
BACKEND_HOST=your-backend-domain.com
BACKEND_PORT=80
FRONTEND_HOST=your-frontend-domain.com
FRONTEND_PORT=80
REACT_APP_API_URL=http://your-backend-domain.com
USE_HTTPS=false
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com
```

### Production Environment (HTTPS)
```bash
# .env file
BACKEND_HOST=your-backend-domain.com
BACKEND_PORT=443
FRONTEND_HOST=your-frontend-domain.com
FRONTEND_PORT=443
REACT_APP_API_URL=https://your-backend-domain.com
USE_HTTPS=true
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com
```

### Docker Compose Configuration
```yaml
# docker-compose.yml environment variables
services:
  backend:
    environment:
      - BACKEND_HOST=backend
      - BACKEND_PORT=8000
      - FRONTEND_HOST=frontend
      - FRONTEND_PORT=3000
      - REACT_APP_API_URL=http://backend:8000
      - USE_HTTPS=false
      - CORS_ALLOWED_ORIGINS=http://frontend:3000
  
  frontend:
    environment:
      - REACT_APP_API_URL=http://backend:8000
```

## 🔍 Key Benefits

### 1. **Environment Flexibility**
- Easy switching between development, staging, and production
- No code changes needed for different environments
- Consistent configuration across all services

### 2. **Security Improvements**
- No hardcoded URLs in source code
- Environment-specific CORS configuration
- HTTPS/HTTP protocol switching

### 3. **Development Experience**
- Easier local development setup
- Consistent proxy configuration
- Clear environment variable documentation

### 4. **Deployment Ready**
- Docker-friendly configuration
- Kubernetes environment variable support
- CI/CD pipeline integration

## 🧪 Testing the Configuration

### 1. Backend Management Commands
```bash
# Test with environment variables
BACKEND_HOST=production.com BACKEND_PORT=443 USE_HTTPS=true python manage.py initialize_platform

# Should output:
# Admin URL: https://production.com:443/admin/
# API URL: https://production.com:443/api/
```

### 2. Frontend Development Server
```bash
# Start with custom API URL
REACT_APP_API_URL=http://localhost:9000 npm start

# Should proxy requests to localhost:9000 instead of default 8000
```

### 3. CORS Configuration
```bash
# Test CORS with environment variables
CORS_ALLOWED_ORIGINS=https://myapp.com,https://staging.myapp.com python manage.py runserver

# Backend should only allow requests from specified origins
```

## 📋 Migration Checklist

- [x] **Frontend Services** - Already environment-aware ✅
- [x] **Backend Settings** - Already environment-aware ✅
- [x] **Management Commands** - Updated with environment variables ✅
- [x] **CORS Configuration** - Environment-driven ✅
- [x] **Test Files** - Environment variables ✅
- [x] **Documentation** - Dynamic URLs ✅
- [x] **Frontend Proxy** - Environment-aware ✅
- [x] **Environment Variables** - Documented in .env.example ✅
- [x] **Duplicate Directory** - Updates applied ✅

## 🎯 Next Steps

1. **Update your `.env` file** with the new environment variables
2. **Restart your development server** to apply changes
3. **Test the configuration** in your target environment
4. **Update Docker configurations** if using containers
5. **Update CI/CD pipelines** with new environment variables

## 📞 Support

If you encounter any issues with the environment variable configuration:

1. Check that all required environment variables are set
2. Verify the format of comma-separated values (no spaces)
3. Ensure URLs don't have trailing slashes unless intended
4. Test CORS configuration in browser developer tools
5. Check management command output for URL generation

---

**Environment Variables Configuration** ✅ Complete
**Production Ready** ✅ Ready
**Documentation** ✅ Comprehensive