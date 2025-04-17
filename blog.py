"""
This file serves as a facade for the blog module
"""
import os
import sys

# Add the django-mini-blog-main directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "django-mini-blog-main"))

# Import the actual blog module
import blog 