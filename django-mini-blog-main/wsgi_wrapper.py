import os
import sys

# Add the django-mini-blog-main directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Import the actual WSGI application
from blog.wsgi import application 