#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Navigate to the correct directory
cd django-mini-blog-main

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate 