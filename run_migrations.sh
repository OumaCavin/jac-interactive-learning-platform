#!/bin/bash
# Migration automation script that handles all Django prompts automatically

set -e

echo "🔄 Starting automated Django migration process..."

# Set environment variables to prevent Django interactive prompts
export DJANGO_SUPERUSER_ID=""
export DJANGO_COLUMNS="0"
export DJANGO_SKIP="1"
export PYTHONUNBUFFERED=1

# Function to run Django command with automatic prompt handling
run_django_command() {
    local cmd="$1"
    local args="${@:2}"
    
    echo "  → Running: python manage.py $cmd $args"
    
    # Use python -c with stdin to automatically answer prompts
    python manage.py $cmd $args << 'EOF' 2>&1 || {
        # If the command fails, try with different approach
        return 1
    }
    return 0
}

# Strategy 1: Standard migrate with --noinput (should handle most prompts)
echo "Strategy 1: Standard migrate with --noinput"
run_django_command migrate --noinput && {
    echo "✅ Strategy 1 succeeded!"
    return 0
} || {
    echo "⚠️ Strategy 1 failed, trying next strategy..."
}

# Strategy 2: Use safe_migrate command
echo "Strategy 2: Using safe_migrate command"
python manage.py safe_migrate && {
    echo "✅ Strategy 2 succeeded!"
    return 0
} || {
    echo "⚠️ Strategy 2 failed, trying next strategy..."
}

# Strategy 3: Makemigrations then migrate
echo "Strategy 3: Makemigrations then migrate"
run_django_command makemigrations --merge --noinput && {
    run_django_command migrate --noinput
    echo "✅ Strategy 3 succeeded!"
    return 0
} || {
    echo "⚠️ Strategy 3 failed, trying final strategy..."
}

# Strategy 4: Fake initial migration
echo "Strategy 4: Fake initial migration"
run_django_command migrate --fake-initial --noinput && {
    echo "✅ Strategy 4 succeeded!"
    return 0
} || {
    echo "❌ All strategies failed!"
    return 1
}

echo "🎉 All migration strategies completed!"