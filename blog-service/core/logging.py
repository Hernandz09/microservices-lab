import json
import logging
from datetime import datetime


class JsonFormatter(logging.Formatter):
    """Formateador para logging en formato JSON."""
    
    def format(self, record):
        log_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
        }
        
        if hasattr(record, 'exc_info') and record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)
        
        return json.dumps(log_data)
