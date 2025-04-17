"""
Minimal urls file for Render deployment
This file simply imports from the real urls
"""
import os
import sys

# Add the django-mini-blog-main directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "django-mini-blog-main"))

# Import urls from the actual urls module
from blog.urls import * 