"""
JSON logger para logs estructurados.
"""
import logging
import json
from datetime import datetime


class JsonFormatter(logging.Formatter):
    """
    Formateador de logs en JSON.
    """
    def format(self, record):
        log_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
        }
        
        # Agregar información adicional si existe
        if hasattr(record, 'extra_data'):
            log_data.update(record.extra_data)
        
        # Agregar información de excepción si existe
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)
        
        return json.dumps(log_data, ensure_ascii=False)
