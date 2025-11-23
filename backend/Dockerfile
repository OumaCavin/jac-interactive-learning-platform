# Django Backend Production Dockerfile
# Multi-stage build for optimized production deployment
# Author: MiniMax Agent

# Stage 1: Dependencies
FROM python:3.11-slim as dependencies

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    gcc \
    libc6-dev \
    libpq-dev \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies with retry, timeout, and fallback mirror
RUN pip install --no-cache-dir --default-timeout=300 --retries=5 \
    -r requirements.txt || \
    (echo "Primary PyPI mirror failed, trying alternative" && \
     pip install --no-cache-dir --default-timeout=300 --retries=5 --index-url https://pypi.douban.com/simple/ -r requirements.txt)

# Stage 2: Application
FROM python:3.11-slim as application

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Create non-root user
RUN groupadd -r jac && useradd -r -g jac jac

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy installed packages from dependencies stage
COPY --from=dependencies /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/
COPY --from=dependencies /usr/local/bin/ /usr/local/bin/

# Copy application code
COPY . .

# Create directories for logs and media
RUN mkdir -p logs media static

# Create inline Python entrypoint to avoid bash script permission issues
RUN echo 'import subprocess' > /tmp/entrypoint.py && \
    echo 'import time' >> /tmp/entrypoint.py && \
    echo 'import socket' >> /tmp/entrypoint.py && \
    echo 'import os' >> /tmp/entrypoint.py && \
    echo '' >> /tmp/entrypoint.py && \
    echo 'print("🚀 Starting JAC Learning Platform...")' >> /tmp/entrypoint.py && \
    echo 'print("📡 Waiting for database...")' >> /tmp/entrypoint.py && \
    echo 'while True:' >> /tmp/entrypoint.py && \
    echo '    try:' >> /tmp/entrypoint.py && \
    echo '        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:' >> /tmp/entrypoint.py && \
    echo '            s.settimeout(1)' >> /tmp/entrypoint.py && \
    echo '            result = s.connect_ex(("postgres", 5432))' >> /tmp/entrypoint.py && \
    echo '            if result == 0:' >> /tmp/entrypoint.py && \
    echo '                break' >> /tmp/entrypoint.py && \
    echo '    except Exception:' >> /tmp/entrypoint.py && \
    echo '        pass' >> /tmp/entrypoint.py && \
    echo '    print("  Database not ready yet, retrying...")' >> /tmp/entrypoint.py && \
    echo '    time.sleep(1)' >> /tmp/entrypoint.py && \
    echo 'print("✅ Database is ready!")' >> /tmp/entrypoint.py && \
    echo 'print("📦 Running platform initialization...")' >> /tmp/entrypoint.py && \
    echo 'subprocess.run(["python", "manage.py", "migrate"], check=False)' >> /tmp/entrypoint.py && \
    echo 'subprocess.run(["python", "manage.py", "initialize_platform", "--username=admin", "--email=admin@jacplatform.com", "--password=admin123"], check=False)' >> /tmp/entrypoint.py && \
    echo 'print("🌐 Starting Django server...")' >> /tmp/entrypoint.py && \
    echo 'os.execvp("python", ["python", "manage.py", "runserver", "0.0.0.0:8000"])' >> /tmp/entrypoint.py

# Change ownership to non-root user
RUN chown -R jac:jac /app

# Switch to non-root user
USER jac

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/health/ || exit 1

# Default command (can be overridden)
CMD ["python", "/tmp/entrypoint.py"]