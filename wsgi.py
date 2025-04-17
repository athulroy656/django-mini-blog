import os
import sys

# Add the django-mini-blog-main directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "django-mini-blog-main")))

# Import the actual WSGI application
from blog.wsgi import application 