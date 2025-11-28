# Quick Reference: Essential Commands That Worked

## One-Line Solutions

### Fix Django Static Files (Run these commands):

```bash
# 1. Stop containers
docker-compose down

# 2. Modify settings as root (nginx container has root access)
docker-compose exec nginx sed -i "s|STATIC_ROOT = Path('/tmp/staticfiles')|STATIC_ROOT = '/var/www/static'|g" /app/config/settings.py

# 3. Start containers
docker-compose up -d

# 4. Wait for containers to be ready, then create directory and collect static files
docker-compose exec nginx mkdir -p /var/www/static
docker-compose exec nginx python manage.py collectstatic --noinput

# 5. Verify static files were created
docker-compose exec nginx ls -la /var/www/static/admin/css/ | head -5
```

### Update Nginx Configuration (Add static file serving):

```bash
# Create nginx config file
cat > /tmp/nginx-static.conf << 'EOF'
server {
    listen 80;
    server_name localhost;

    location / {
        root /usr/share/nginx/html;
        index index.html index.htm;
        try_files $uri $uri/ @backend;
    }

    location @backend {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /var/www/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    error_page 500 502 503 504 /50x.html;
    location = /50x.html {
        root /usr/share/nginx/html;
    }
}
EOF

# Copy to nginx container
docker cp /tmp/nginx-static.conf nginx:/etc/nginx/conf.d/default.conf

# Test and reload nginx
docker-compose exec nginx nginx -t
docker-compose exec nginx nginx -s reload
```

### Test Everything is Working:

```bash
# Test frontend login
curl -I http://localhost:3000/login

# Test static files via nginx
curl -I http://localhost/static/admin/css/base.css

# Test Django admin via nginx
curl -I http://localhost/admin/

# Test Django admin direct
curl -I http://localhost:8000/admin/
```

## Expected Results:
- **Frontend Login**: HTTP 200 OK
- **Static Files**: HTTP 200 OK (Content-Type: text/css)
- **Django Admin**: HTTP 200 OK
- **Admin Direct**: HTTP 302 Found (redirects to login)

## Files That Were Modified:
1. `backend/config/settings.py` - STATIC_ROOT changed to '/var/www/static'
2. `nginx/nginx.conf` - Added static file location block

## Commit Changes:
```bash
git add backend/config/settings.py
git commit -m "Fix static files: Use /var/www/static for Django static files"
git push origin main
```