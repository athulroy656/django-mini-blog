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
            
            # Ensure ALLOWED_HOSTS is properly set for Render
            if 'ALLOWED_HOSTS' in modified_content:
                import re
                allowed_hosts_pattern = r'ALLOWED_HOSTS\s*=\s*\[(.*?)\]'
                match = re.search(allowed_hosts_pattern, modified_content, re.DOTALL)
                if match:
                    current_hosts = match.group(1)
                    render_hosts = "'*', 'sblog-zpji.onrender.com', '.onrender.com'"
                    if not any(host in current_hosts for host in ["'*'", "'.onrender.com'", "'sblog-zpji.onrender.com'"]):
                        new_hosts = f"ALLOWED_HOSTS = [{current_hosts}, {render_hosts}]"
                        modified_content = re.sub(allowed_hosts_pattern, new_hosts, modified_content, flags=re.DOTALL)
            else:
                # If ALLOWED_HOSTS is not defined, add it
                modified_content += "\n# Added by deployment script\nALLOWED_HOSTS = ['*', 'sblog-zpji.onrender.com', '.onrender.com']\n"
            
            # Execute the modified content
            exec(modified_content)
        else:
            # Execute original content if no modification needed
            exec(content)
            
        # Force update ALLOWED_HOSTS after execution
        import django.conf
        django.conf.settings.ALLOWED_HOSTS = list(set(
            getattr(django.conf.settings, 'ALLOWED_HOSTS', []) + 
            ['*', 'sblog-zpji.onrender.com', '.onrender.com', 'localhost', '127.0.0.1']
        ))
        
    else:
        raise ImportError(f"Cannot find settings module at {real_settings_module}")
        
except Exception as e:
    logger.error(f"Error importing settings: {e}")
    
    # Define minimal settings to get Django running
    import django.conf
    
    # Create minimal settings
    DEBUG = os.environ.get('DEBUG', 'True') == 'True'
    SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-default-key-for-development')
    ALLOWED_HOSTS = ['*', 'sblog-zpji.onrender.com', '.onrender.com', 'localhost', '127.0.0.1']
    
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
        'app',
        'corsheaders',
    ]
    
    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'whitenoise.middleware.WhiteNoiseMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'corsheaders.middleware.CorsMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]
    
    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.join(project_dir, 'app', 'templates')],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]
    
    # Set these minimal settings
    settings = django.conf.Settings(settings_module=None)
    for key, value in locals().items():
        if key.isupper():
            setattr(settings, key, value)
    django.conf.settings = settings 