"""
Django settings for blog project.
This file imports settings from the real Django project.
"""

import os
import sys
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the django-mini-blog-main directory to Python path
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
project_dir = os.path.join(current_dir, "django-mini-blog-main")
sys.path.insert(0, project_dir)

# Try to manually define required settings if importing fails
try:
    # Import all settings from the real settings module
    from django.conf import settings
    
    # Import all settings attributes from the real settings module
    real_settings_module = os.path.join(project_dir, "blog", "settings.py")
    if os.path.exists(real_settings_module):
        # Read the file content
        with open(real_settings_module, 'r') as f:
            content = f.read()
            
        # Replace problematic imports
        if 'import dj_database_url' in content:
            modified_content = content.replace('import dj_database_url', 
                                              'try:\n    import dj_database_url\nexcept ImportError:\n    dj_database_url = None')
            
            # Also handle dj_database_url usage
            if 'dj_database_url.config' in modified_content:
                modified_content = modified_content.replace('dj_database_url.config', 
                                                           '(dj_database_url.config if dj_database_url else lambda **kw: {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": os.path.join(BASE_DIR, "db.sqlite3")}})')
            
            # Execute the modified content
            exec(modified_content)
        else:
            # Execute original content if no modification needed
            exec(content)
    else:
        raise ImportError(f"Cannot find settings module at {real_settings_module}")
        
except Exception as e:
    logger.error(f"Error importing settings: {e}")
    
    # Define minimal settings to get Django running
    import django.conf
    
    # Create minimal settings
    DEBUG = os.environ.get('DEBUG', 'True') == 'True'
    SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-default-key-for-development')
    ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')
    
    # Database settings
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(current_dir, 'db.sqlite3'),
        }
    }
    
    # Basic installed apps
    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
    ]
    
    # Set these minimal settings
    settings = django.conf.Settings(settings_module=None)
    for key, value in locals().items():
        if key.isupper():
            setattr(settings, key, value)
    django.conf.settings = settings 