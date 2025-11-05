"""
Tareas asíncronas de Celery para envío de emails y notificaciones.
"""
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
import logging

from .models import ContactMessage, NotificationLog
from utils.mailer import send_email

logger = logging.getLogger('notifications')


@shared_task(bind=True, max_retries=3, default_retry_delay=5)
def send_contact_email_task(self, contact_message_id):
    """
    Tarea asíncrona para enviar email de mensaje de contacto.
    
    Args:
        contact_message_id: UUID del mensaje de contacto
    """
    try:
        message = ContactMessage.objects.get(id=contact_message_id)
        
        # Marcar como en cola
        message.mark_as_queued()
        
        # Preparar email
        subject = f"Nuevo mensaje de contacto de {message.name}"
        body = f"""
        Nuevo mensaje de contacto recibido:
        
        Nombre: {message.name}
        Email: {message.email}
        
        Mensaje:
        {message.message}
        
        ---
        Enviado desde Email Service
        """
        
        # Enviar email
        success = send_email(
            to=[settings.DEFAULT_FROM_EMAIL],
            subject=subject,
            body=body,
            from_email=message.email
        )
        
        if success:
            message.mark_as_sent()
            logger.info(f"Contact message {contact_message_id} sent successfully")
            return {'status': 'sent', 'message_id': str(contact_message_id)}
        else:
            raise Exception("Failed to send email")
            
    except ContactMessage.DoesNotExist:
        logger.error(f"Contact message {contact_message_id} not found")
        return {'status': 'error', 'message': 'Contact message not found'}
    
    except Exception as exc:
        logger.error(f"Error sending contact message {contact_message_id}: {str(exc)}")
        
        try:
            message.mark_as_failed(str(exc))
        except:
            pass
        
        # Reintentar la tarea
        raise self.retry(exc=exc)


@shared_task(bind=True, max_retries=3, default_retry_delay=5)
def send_notification_task(self, notification_id):
    """
    Tarea asíncrona para enviar notificación.
    
    Args:
        notification_id: UUID de la notificación
    """
    try:
        notification = NotificationLog.objects.get(id=notification_id)
        
        # Marcar como en cola
        notification.mark_as_queued()
        
        # Enviar según el tipo
        if notification.notification_type == 'email':
            success = send_email(
                to=[notification.to],
                subject=notification.subject,
                body=notification.body
            )
        else:
            # Otros tipos de notificación (SMS, Push) se implementarían aquí
            logger.warning(f"Notification type {notification.notification_type} not implemented yet")
            success = True  # Por ahora marcamos como exitoso
        
        if success:
            notification.mark_as_sent()
            logger.info(f"Notification {notification_id} sent successfully")
            return {'status': 'sent', 'notification_id': str(notification_id)}
        else:
            raise Exception("Failed to send notification")
            
    except NotificationLog.DoesNotExist:
        logger.error(f"Notification {notification_id} not found")
        return {'status': 'error', 'message': 'Notification not found'}
    
    except Exception as exc:
        logger.error(f"Error sending notification {notification_id}: {str(exc)}")
        
        try:
            notification.mark_as_failed(str(exc))
        except:
            pass
        
        # Reintentar la tarea
        raise self.retry(exc=exc)
