"""
Custom middleware to handle host validation
"""

class AllowAllHostsMiddleware:
    """
    A middleware that allows all hosts, bypassing Django's host validation.
    This is risky in production, but useful for deployment troubleshooting.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # Save the original get_host method
        original_get_host = request.get_host
        
        # Override get_host to avoid host validation
        def get_host_override():
            try:
                return original_get_host()
            except Exception:
                # Get the host from the request headers
                return request.META.get('HTTP_HOST', 'localhost')
        
        # Replace the method
        request.get_host = get_host_override
        
        # Process request and get response
        response = self.get_response(request)
        
        # Restore original method (not strictly necessary, but good practice)
        request.get_host = original_get_host
        
        return response 