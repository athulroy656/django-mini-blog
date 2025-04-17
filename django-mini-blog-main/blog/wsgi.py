"""
WSGI config for blog project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog.settings')

# Override ALLOWED_HOSTS
os.environ['ALLOWED_HOSTS'] = '*,sblog-zpji.onrender.com,localhost,127.0.0.1,.onrender.com'

application = get_wsgi_application()

# Force ALLOWED_HOSTS after application is loaded
try:
    from django.conf import settings
    if hasattr(settings, 'ALLOWED_HOSTS'):
        settings.ALLOWED_HOSTS = ['*', 'sblog-zpji.onrender.com', 'localhost', '127.0.0.1', '.onrender.com']
except Exception as e:
    print(f"Error setting ALLOWED_HOSTS: {e}")
