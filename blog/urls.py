"""
URL Configuration for blog project.
This file imports URLs from the real Django project.
"""

import os
import sys
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the django-mini-blog-main directory to Python path
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
project_dir = os.path.join(current_dir, "django-mini-blog-main")
sys.path.insert(0, project_dir)

# Import all URL patterns from the real project
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

try:
    # Try to get the app's urls
    sys.path.insert(0, os.path.join(project_dir, 'app'))
    from app.views import home

    # Define root URL pattern
    urlpatterns = [
        path('admin/', admin.site.urls),
        path('', home, name='home'),
    ]
    
    # Try to import the real urlpatterns
    try:
        real_urls_module = os.path.join(project_dir, "blog", "urls.py")
        if os.path.exists(real_urls_module):
            with open(real_urls_module, 'r') as f:
                content = f.read()
                
            # Extract urlpatterns if possible
            import re
            pattern = r'urlpatterns\s*=\s*\[(.*?)\]'
            match = re.search(pattern, content, re.DOTALL)
            if match:
                # Append real paths
                exec(f"real_urlpatterns = [{match.group(1)}]")
                urlpatterns.extend(real_urlpatterns)
            else:
                # Try to import from blog.urls
                from django_mini_blog_main.blog.urls import urlpatterns as real_urlpatterns
                urlpatterns.extend(real_urlpatterns)
    except Exception as e:
        logger.error(f"Failed to import real urlpatterns: {e}")
        # Note: Using the default urlpatterns defined above
    
    # Add static/media serving
    if settings.DEBUG:
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
        
except Exception as e:
    logger.error(f"Failed to define URL patterns: {e}")
    
    # Define basic URL patterns
    urlpatterns = [
        path('admin/', admin.site.urls),
        re_path(r'^$', RedirectView.as_view(url='/admin/'), name='home'),
    ]
    
    # Add static serving
    if hasattr(settings, 'STATIC_URL') and hasattr(settings, 'STATIC_ROOT'):
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    if hasattr(settings, 'MEDIA_URL') and hasattr(settings, 'MEDIA_ROOT'):
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 