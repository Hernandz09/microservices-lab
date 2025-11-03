import json
import logging
import time
from django.utils.deprecation import MiddlewareMixin


class RequestLoggingMiddleware(MiddlewareMixin):
    """Middleware para logging estructurado de requests en formato JSON."""
    
    def process_request(self, request):
        request._start_time = time.time()
        return None
    
    def process_response(self, request, response):
        if hasattr(request, '_start_time'):
            duration = time.time() - request._start_time
            log_data = {
                'method': request.method,
                'path': request.path,
                'status_code': response.status_code,
                'duration_ms': round(duration * 1000, 2),
                'user_agent': request.META.get('HTTP_USER_AGENT', ''),
            }
            logger = logging.getLogger('django.request')
            logger.info(json.dumps(log_data))
        return response


class AuthTokenLoggingMiddleware(MiddlewareMixin):
    """Middleware que lee el header Authorization para preparar integración futura con Auth."""
    
    def process_request(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if auth_header:
            logger = logging.getLogger('django')
            logger.info(f"Authorization header detected: {auth_header[:20]}... (will be validated in Day 4)")
        return None
