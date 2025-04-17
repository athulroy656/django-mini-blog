#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Make migrations to ensure model changes are captured
echo "Making migrations..."
python manage.py makemigrations app

# Run migrations
echo "Running migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --no-input

# Create a superuser if one doesn't exist (optional)
echo "Attempting to create a superuser..."
echo "from app.models import User; User.objects.filter(is_superuser=True).exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell || true 