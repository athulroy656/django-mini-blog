#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Navigate to the correct directory
cd django-mini-blog-main

# Create a sample data python file if it doesn't exist
if [ ! -f sample_data.py ]; then
    echo "Creating sample data script..."
    touch sample_data.py
fi

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
echo "from app.models import User; User.objects.filter(is_superuser=True).exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell || true

# Load sample data
echo "Loading sample data..."
python sample_data.py || true 