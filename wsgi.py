"""
Root level WSGI entry point, importing from either the blog package directly
or from django-mini-blog-main/blog depending on what works.
"""

import os
import sys
import logging

# Setup basic logging to help troubleshoot
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
logger.info(f"Current directory: {current_dir}")

# Add project directories to Python path
project_dir = os.path.join(current_dir, "django-mini-blog-main")
sys.path.insert(0, current_dir)
sys.path.insert(0, project_dir)

logger.info(f"Python path updated with: {current_dir}, {project_dir}")

try:
    # First try to import from the local blog package
    logger.info("Trying to import from local blog package...")
    from blog.wsgi import application
    logger.info("Successfully imported application from local blog.wsgi")
except ImportError as e:
    logger.error(f"Failed to import from local blog.wsgi: {e}")
    
    try:
        # Try to import from django-mini-blog-main/blog
        logger.info("Trying to import from django-mini-blog-main/blog...")
        sys.path.insert(0, os.path.join(project_dir, "blog"))
        from django_mini_blog_main.blog.wsgi import application
        logger.info("Successfully imported application from django_mini_blog_main.blog.wsgi")
    except ImportError as e2:
        logger.error(f"Failed to import from django_mini_blog_main.blog.wsgi: {e2}")
        
        # List directories to debug
        try:
            logger.info(f"Contents of {current_dir}: {os.listdir(current_dir)}")
            if os.path.exists(project_dir):
                logger.info(f"Contents of {project_dir}: {os.listdir(project_dir)}")
                
            # Check if the blog directory exists
            blog_dir = os.path.join(current_dir, "blog")
            if os.path.exists(blog_dir):
                logger.info(f"Contents of {blog_dir}: {os.listdir(blog_dir)}")
                
            # Check if the project blog directory exists
            project_blog_dir = os.path.join(project_dir, "blog")
            if os.path.exists(project_blog_dir):
                logger.info(f"Contents of {project_blog_dir}: {os.listdir(project_blog_dir)}")
        except Exception as dir_error:
            logger.error(f"Error listing directories: {dir_error}")
        
        # Raise the original exception
        raise e 