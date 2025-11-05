"""
Middleware para logging de requests y otras utilidades.
"""
import time
import logging
import json

logger = logging.getLogger('django.request')


class RequestLoggingMiddleware:
    """
    Middleware que loguea información de cada request en formato JSON.
    """
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Timestamp de inicio
        start_time = time.time()
        
        # Procesar request
        response = self.get_response(request)
        
        # Calcular duración
        duration_ms = (time.time() - start_time) * 1000
        
        # Preparar log data
        log_data = {
            'method': request.method,
            'path': request.path,
            'status_code': response.status_code,
            'duration_ms': round(duration_ms, 2),
            'user_agent': request.META.get('HTTP_USER_AGENT', ''),
        }
        
        # Loguear
        if response.status_code >= 500:
            logger.error(json.dumps(log_data, ensure_ascii=False))
        elif response.status_code >= 400:
            logger.warning(json.dumps(log_data, ensure_ascii=False))
        else:
            logger.info(json.dumps(log_data, ensure_ascii=False))
        
        return response


class AuthTokenLoggingMiddleware:
    """
    Middleware que captura y loguea el header Authorization (preparación para JWT).
    """
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        
        if auth_header:
            # Solo loguear que existe, no el contenido completo (seguridad)
            logger.info(f"Authorization header detected: {auth_header[:20]}... (will be validated in future)")
        
        response = self.get_response(request)
        return response
