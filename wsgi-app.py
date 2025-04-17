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
logger.info(f"Full sys.path: {sys.path}")

try:
    # Try importing from the blog module
    from blog.wsgi import application
    logger.info("Successfully imported application from blog.wsgi")
except ImportError as e:
    logger.error(f"Failed to import from blog.wsgi: {e}")
    
    # List directories to debug
    try:
        logger.info(f"Contents of {current_dir}: {os.listdir(current_dir)}")
        logger.info(f"Contents of {project_dir}: {os.listdir(project_dir)}")
    except Exception as dir_error:
        logger.error(f"Error listing directories: {dir_error}")
    
    # Try to find wsgi.py files
    for root, dirs, files in os.walk(current_dir):
        if "wsgi.py" in files:
            logger.info(f"Found wsgi.py in: {root}")
    
    raise 