"""
Minimal settings file for Render deployment
This file simply imports from the real settings
"""
import os
import sys

# Add the django-mini-blog-main directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "django-mini-blog-main"))

# Import settings from the actual settings module
from blog.settings import * 