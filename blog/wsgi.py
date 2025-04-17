"""
WSGI config for blog project.
"""

import os
import sys
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the django-mini-blog-main directory to the Python path
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
project_dir = os.path.join(current_dir, "django-mini-blog-main")
sys.path.insert(0, project_dir)

logger.info(f"Current directory: {current_dir}")
logger.info(f"Project directory: {project_dir}")
logger.info(f"Python path: {sys.path}")

try:
    # Import the real wsgi application
    from django.core.wsgi import get_wsgi_application
    
    # The real Django settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog.settings')
    
    # Get the application
    application = get_wsgi_application()
    logger.info("Successfully created WSGI application")
except Exception as e:
    logger.error(f"Failed to create WSGI application: {e}")
    
    # Debugging information
    try:
        logger.info(f"Contents of {current_dir}: {os.listdir(current_dir)}")
        logger.info(f"Contents of {project_dir}: {os.listdir(project_dir)}")
        
        # Check if the blog module exists in the project directory
        project_blog_dir = os.path.join(project_dir, "blog")
        if os.path.exists(project_blog_dir):
            logger.info(f"Contents of {project_blog_dir}: {os.listdir(project_blog_dir)}")
    except Exception as debug_error:
        logger.error(f"Error while debugging: {debug_error}")
    
    # Re-raise the exception
    raise 