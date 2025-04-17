"""
Django settings for blog project.
This file imports settings from the real Django project.
"""

import os
import sys

# Add the django-mini-blog-main directory to Python path
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
project_dir = os.path.join(current_dir, "django-mini-blog-main")
sys.path.insert(0, project_dir)

# Import all settings from the real settings module
from django.conf import settings

# Import all settings attributes from the real settings module
real_settings_module = os.path.join(project_dir, "blog", "settings.py")
if os.path.exists(real_settings_module):
    with open(real_settings_module) as f:
        exec(f.read())
else:
    raise ImportError(f"Cannot find settings module at {real_settings_module}") 