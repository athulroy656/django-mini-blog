"""
WSGI config for blog project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
import sys
import logging

logger = logging.getLogger(__name__)

# Set RENDER environment variable
os.environ['RENDER'] = 'True'

# Override ALLOWED_HOSTS
os.environ['ALLOWED_HOSTS'] = '*,sblog-zpji.onrender.com,localhost,127.0.0.1,.onrender.com'

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog.settings')

# Try to create database tables before application starts
try:
    logger.info("Setting up database from WSGI...")
    from django.db import connection
    
    with connection.cursor() as cursor:
        # Check if BlogPost table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='app_blogpost';")
        if not cursor.fetchone():
            logger.info("BlogPost table doesn't exist, running migrations...")
            from django.core.management import call_command
            call_command('makemigrations', 'app')
            call_command('migrate')
except Exception as e:
    logger.error(f"Error setting up database: {e}")

application = get_wsgi_application()

# Force ALLOWED_HOSTS after application is loaded
try:
    from django.conf import settings
    if hasattr(settings, 'ALLOWED_HOSTS'):
        settings.ALLOWED_HOSTS = ['*', 'sblog-zpji.onrender.com', 'localhost', '127.0.0.1', '.onrender.com']
except Exception as e:
    logger.error(f"Error setting ALLOWED_HOSTS: {e}")
