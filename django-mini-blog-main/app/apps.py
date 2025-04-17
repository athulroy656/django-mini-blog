from django.apps import AppConfig
import logging
import os

logger = logging.getLogger(__name__)


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'
    
    def ready(self):
        # Only run in server mode (not during management commands)
        if os.environ.get('RUN_MAIN') != 'true' and os.environ.get('RENDER'):
            try:
                logger.info("Initializing app on startup...")
                # Set an environment variable to indicate we're on Render
                os.environ['RENDER'] = 'True'
                
                # Import and run the database check function
                from . import views
                views.ensure_tables_exist()
            except Exception as e:
                logger.error(f"Error during app initialization: {e}")
