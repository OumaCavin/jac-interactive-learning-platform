# Django Backend Production Dockerfile
# Multi-stage build for optimized production deployment
# Author: Cavin Otieno

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

# Create non-root user for package installation with proper home directory
RUN groupadd -r jac && \
    useradd -r -g jac -m -d /home/jac jac && \
    chmod 755 /home/jac

# Set work directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies as non-root user with virtual environment
USER jac
# Ensure home directory is writable and create virtual environment
RUN mkdir -p /home/jac && \
    python -m venv /home/jac/venv && \
    /home/jac/venv/bin/pip install --upgrade pip && \
    /home/jac/venv/bin/pip install --no-cache-dir --default-timeout=300 --retries=5 \
    -r requirements.txt || \
    (echo "Primary PyPI mirror failed, trying alternative" && \
     /home/jac/venv/bin/pip install --no-cache-dir --default-timeout=300 --retries=5 --index-url https://pypi.douban.com/simple/ -r requirements.txt)

# Stage 2: Application
FROM python:3.11-slim as application

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Create non-root user with proper home directory
RUN groupadd -r jac && \
    useradd -r -g jac -m -d /home/jac jac && \
    chmod 755 /home/jac

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy installed packages and virtual environment from dependencies stage
COPY --from=dependencies /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/
COPY --from=dependencies /usr/local/bin/ /usr/local/bin/
# Copy the virtual environment from the dependencies stage
COPY --from=dependencies --chown=jac:jac /home/jac/venv /home/jac/venv

# Switch to non-root user for file operations
USER jac

# Copy application code
COPY --chown=jac:jac . .

# Create directories for logs and media
RUN mkdir -p logs media static

# Set Python path to use the virtual environment
ENV PATH="/home/jac/venv/bin:/usr/local/bin:$PATH"
ENV PYTHONPATH="/home/jac/venv/lib/python3.11/site-packages:$PYTHONPATH"

# Switch back to root to create entrypoint (but keep ownership correct)
USER root

# Create production-ready entrypoint
RUN echo 'import subprocess' > /tmp/entrypoint.py && \
    echo 'import time' >> /tmp/entrypoint.py && \
    echo 'import socket' >> /tmp/entrypoint.py && \
    echo 'import os' >> /tmp/entrypoint.py && \
    echo 'import sys' >> /tmp/entrypoint.py && \
    echo 'import glob' >> /tmp/entrypoint.py && \
    echo '' >> /tmp/entrypoint.py && \
    echo 'def find_python_executable():' >> /tmp/entrypoint.py && \
    echo '    # Try primary location for python executable' >> /tmp/entrypoint.py && \
    echo '    possible_paths = [' >> /tmp/entrypoint.py && \
    echo '        "/home/jac/venv/bin/python",' >> /tmp/entrypoint.py && \
    echo '        "/usr/local/bin/python"' >> /tmp/entrypoint.py && \
    echo '    ]' >> /tmp/entrypoint.py && \
    echo '    for path in possible_paths:' >> /tmp/entrypoint.py && \
    echo '        if os.path.exists(path):' >> /tmp/entrypoint.py && \
    echo '            return path' >> /tmp/entrypoint.py && \
    echo '    # Fallback to system python' >> /tmp/entrypoint.py && \
    echo '    return "python"' >> /tmp/entrypoint.py && \
    echo '' >> /tmp/entrypoint.py && \
    echo 'def wait_for_database(max_retries=30):' >> /tmp/entrypoint.py && \
    echo '    print("🚀 Starting JAC Learning Platform Backend...")' >> /tmp/entrypoint.py && \
    echo '    print("📡 Waiting for database connection...")' >> /tmp/entrypoint.py && \
    echo '    for i in range(max_retries):' >> /tmp/entrypoint.py && \
    echo '        try:' >> /tmp/entrypoint.py && \
    echo '            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:' >> /tmp/entrypoint.py && \
    echo '                s.settimeout(2)' >> /tmp/entrypoint.py && \
    echo '                result = s.connect_ex(("postgres", 5432))' >> /tmp/entrypoint.py && \
    echo '                if result == 0:' >> /tmp/entrypoint.py && \
    echo '                    print("✅ Database connection established!")' >> /tmp/entrypoint.py && \
    echo '                    return True' >> /tmp/entrypoint.py && \
    echo '        except Exception as e:' >> /tmp/entrypoint.py && \
    echo '            print(f"  Database check {i+1}/{max_retries} failed: {e}")' >> /tmp/entrypoint.py && \
    echo '        time.sleep(2)' >> /tmp/entrypoint.py && \
    echo '    print("⚠️ Database connection timeout, continuing anyway...")' >> /tmp/entrypoint.py && \
    echo '    return False' >> /tmp/entrypoint.py && \
    echo '' >> /tmp/entrypoint.py && \
    echo 'def start_application():' >> /tmp/entrypoint.py && \
    echo '    python_exe = find_python_executable()' >> /tmp/entrypoint.py && \
    echo '    print(f"🐍 Using Python: {python_exe}")' >> /tmp/entrypoint.py && \
    echo '    wait_for_database()' >> /tmp/entrypoint.py && \
    echo '    print("📦 Running database migrations...")' >> /tmp/entrypoint.py && \
    echo '    try:' >> /tmp/entrypoint.py && \
    echo '        result = subprocess.run([' >> /tmp/entrypoint.py && \
    echo '            python_exe, "manage.py", "migrate", "--noinput"' >> /tmp/entrypoint.py && \
    echo '        ], check=False, capture_output=True, text=True, timeout=60)' >> /tmp/entrypoint.py && \
    echo '        if result.returncode == 0:' >> /tmp/entrypoint.py && \
    echo '            print("✅ Database migrations completed")' >> /tmp/entrypoint.py && \
    echo '        else:' >> /tmp/entrypoint.py && \
    echo '            print("⚠️ Migration warnings (continuing):", result.stderr)' >> /tmp/entrypoint.py && \
    echo '    except Exception as e:' >> /tmp/entrypoint.py && \
    echo '        print(f"⚠️ Migration error: {e} (continuing anyway)")' >> /tmp/entrypoint.py && \
    echo '    print("🌐 Starting Django application server...")' >> /tmp/entrypoint.py && \
    echo '    sys.stdout.flush()' >> /tmp/entrypoint.py && \
    echo '    os.execvp(python_exe, [python_exe, "manage.py", "runserver", "0.0.0.0:8000"])' >> /tmp/entrypoint.py && \
    echo '' >> /tmp/entrypoint.py && \
    echo 'if __name__ == "__main__":' >> /tmp/entrypoint.py && \
    echo '    # Fix permissions for static files directory' >> /tmp/entrypoint.py && \
    echo '    import os' >> /tmp/entrypoint.py && \
    echo '    static_dir = "/var/www/static"' >> /tmp/entrypoint.py && \
    echo '    try:' >> /tmp/entrypoint.py && \
    echo '        os.makedirs(static_dir, exist_ok=True)' >> /tmp/entrypoint.py && \
    echo '        os.system(f"chown -R jac:jac {static_dir}")' >> /tmp/entrypoint.py && \
    echo '        os.system(f"chmod -R 755 {static_dir}")' >> /tmp/entrypoint.py && \
    echo '        print(f"✅ Static files directory permissions fixed: {static_dir}")' >> /tmp/entrypoint.py && \
    echo '    except Exception as e:' >> /tmp/entrypoint.py && \
    echo '        print(f"⚠️ Warning: Could not fix static directory permissions: {e}")' >> /tmp/entrypoint.py && \
    echo '    start_application()' >> /tmp/entrypoint.py

# Change ownership to non-root user
RUN chown -R jac:jac /app /tmp/entrypoint.py

# Switch to non-root user
USER jac

# Expose port
EXPOSE 8000

# Create health check script
RUN echo '#!/bin/bash' > /tmp/healthcheck.sh && \
    echo 'curl -f http://localhost:8000/api/health/static/ > /dev/null 2>&1 && exit 0 || curl -f http://localhost:8000/api/health/simple/ > /dev/null 2>&1 && exit 0 || curl -f http://localhost:8000/api/health/ > /dev/null 2>&1 && exit 0 || exit 1' >> /tmp/healthcheck.sh && \
    chmod +x /tmp/healthcheck.sh

# Health check - using simple curl-based approach
HEALTHCHECK --interval=45s --timeout=10s --start-period=90s --retries=5 \
    CMD /tmp/healthcheck.sh

# Default command (can be overridden)
CMD ["python", "/tmp/entrypoint.py"]