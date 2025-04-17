#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files
cd django-mini-blog-main && python manage.py collectstatic --no-input

# Run migrations
cd django-mini-blog-main && python manage.py migrate 