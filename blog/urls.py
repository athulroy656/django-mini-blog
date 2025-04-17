"""
URL Configuration for blog project.
This file imports URLs from the real Django project.
"""

import os
import sys

# Add the django-mini-blog-main directory to Python path
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
project_dir = os.path.join(current_dir, "django-mini-blog-main")
sys.path.insert(0, project_dir)

# Import all URL patterns from the real project
from django.contrib import admin
from django.urls import path, include

try:
    # Try to import urlpatterns from the real project
    from django_mini_blog_main.blog.urls import urlpatterns
except ImportError:
    # Define fallback URL patterns
    urlpatterns = [
        path('admin/', admin.site.urls),
    ] 