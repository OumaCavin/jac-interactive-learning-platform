# SSL Certificates Directory

This directory is used to store SSL/TLS certificates for HTTPS support.

## Usage:
- Place your SSL certificates (`.crt`, `.key`) files in this directory
- Update `nginx.conf` to reference the correct certificate paths if using HTTPS

## Default Setup:
- HTTP is currently enabled on port 80
- HTTPS configuration is ready but requires valid certificates
