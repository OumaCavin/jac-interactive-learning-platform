# JAC Learning Platform - Credentials to Update

**🚨 IMPORTANT: Replace these default credentials before production deployment**

---

## 🔑 **ENVIRONMENT VARIABLES (.env file)**

| Variable | Current Value | Replace With | Purpose |
|----------|---------------|--------------|---------|
| `SECRET_KEY` | `django-insecure-production-key` | **Strong random 50+ character key** | Django security |
| `REDIS_PASSWORD` | `redis_password` | **Strong random password** | Redis authentication |
| `POSTGRES_PASSWORD` | `jac_password` | **Strong random password** | Database access |
| `EMAIL_HOST_USER` | `your-email@example.com` | **Your actual email address** | SMTP authentication |
| `EMAIL_HOST_PASSWORD` | `your-app-password` | **App-specific password** | Email sending |
| `SENTRY_DSN` | `your-sentry-dsn-here` | **Your Sentry DSN** | Error monitoring |
| `CORS_ALLOWED_ORIGINS` | `http://localhost:3000` | **Your production domain(s)** | Cross-origin requests |

---

## 👤 **USER ACCOUNTS**

### **Demo User (Change immediately)**
- **Email:** `demo@example.com`
- **Password:** `demo123`
- **Action:** Change password or disable account

### **Admin User**
- **Username:** `admin`
- **Password:** `admin123`
- **Action:** Change password after first login

---

## 🗄️ **DATABASE CREDENTIALS**

| Service | Username | Current Password | **NEW PASSWORD** |
|---------|----------|------------------|------------------|
| PostgreSQL | `jac_user` | `jac_password` | **Strong random password** |
| Redis | (none) | `redis_password` | **Strong random password** |

---

## 🔒 **SSL CERTIFICATES (HTTPS Required)**

| File | Location | Status | **REQUIRED FOR HTTPS** |
|------|----------|--------|------------------------|
| SSL Certificate | `./nginx/ssl/cert.pem` | Placeholder | **Your SSL certificate** |
| Private Key | `./nginx/ssl/key.pem` | Placeholder | **Your SSL private key** |

---

## 📧 **EMAIL CONFIGURATION**

**Update these in `.env` file:**
- `EMAIL_HOST` - Your SMTP server (e.g., smtp.gmail.com)
- `EMAIL_PORT` - Usually 587 (TLS) or 465 (SSL)
- `EMAIL_HOST_USER` - Your email address
- `EMAIL_HOST_PASSWORD` - App-specific password
- `EMAIL_USE_TLS` - Usually `True`

---

## 🔄 **QUICK CREDENTIAL UPDATE COMMANDS**

### **Generate Secure Passwords:**
```bash
# Generate random password
openssl rand -base64 32

# Generate Django secret key
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### **Update .env file:**
```bash
# Edit the .env file with new credentials
nano .env

# Or create new .env from template
cp .env.example .env
# Then edit .env with secure values
```

---

## ✅ **POST-DEPLOYMENT CHECKLIST**

- [ ] All environment variables updated with secure values
- [ ] SSL certificates configured for HTTPS
- [ ] Email settings configured for notifications
- [ ] Default user passwords changed
- [ ] Admin account secured
- [ ] Sentry error monitoring configured
- [ ] Domain properly configured in CORS settings
- [ ] Database backups configured

---

**🔐 SECURITY REMINDER: Never use the default credentials in production!**