"""
Views para el servicio de notificaciones.
"""
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
import logging

from .models import ContactMessage, NotificationLog
from .serializers import (
    ContactMessageSerializer, 
    ContactMessageListSerializer,
    NotificationSerializer,
    NotificationListSerializer
)
from .tasks import send_contact_email_task, send_notification_task

logger = logging.getLogger('notifications')


class ContactMessageViewSet(mixins.CreateModelMixin,
                           mixins.ListModelMixin,
                           mixins.RetrieveModelMixin,
                           viewsets.GenericViewSet):
    """
    ViewSet para mensajes de contacto.
    
    POST /api/contact/ - Crear nuevo mensaje de contacto
    GET /api/contact/ - Listar mensajes de contacto
    GET /api/contact/{id}/ - Obtener detalle de mensaje
    """
    queryset = ContactMessage.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ContactMessageListSerializer
        return ContactMessageSerializer
    
    def create(self, request, *args, **kwargs):
        """
        Crear un nuevo mensaje de contacto y encolarlo para envío.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Guardar mensaje
        contact_message = serializer.save()
        
        # Encolar tarea de envío (asíncrono con Celery)
        try:
            send_contact_email_task.delay(str(contact_message.id))
            contact_message.mark_as_queued()
            logger.info(f"Contact message {contact_message.id} queued for sending")
        except Exception as e:
            logger.error(f"Error queuing contact message: {str(e)}")
            # Si falla Celery, al menos guardamos el mensaje
        
        return Response(
            {
                'id': contact_message.id,
                'status': 'queued',
                'message': 'Mensaje recibido y encolado para envío'
            },
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """
        Estadísticas de mensajes de contacto.
        GET /api/contact/stats/
        """
        total = ContactMessage.objects.count()
        pending = ContactMessage.objects.filter(status='pending').count()
        queued = ContactMessage.objects.filter(status='queued').count()
        sent = ContactMessage.objects.filter(status='sent').count()
        failed = ContactMessage.objects.filter(status='failed').count()
        
        return Response({
            'total': total,
            'pending': pending,
            'queued': queued,
            'sent': sent,
            'failed': failed
        })


class NotificationViewSet(mixins.CreateModelMixin,
                         mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         viewsets.GenericViewSet):
    """
    ViewSet para notificaciones (endpoint interno para otros servicios).
    
    POST /api/notify/ - Crear nueva notificación
    GET /api/notify/ - Listar notificaciones
    GET /api/notify/{id}/ - Obtener detalle de notificación
    """
    queryset = NotificationLog.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'list':
            return NotificationListSerializer
        return NotificationSerializer
    
    def create(self, request, *args, **kwargs):
        """
        Crear una nueva notificación y encolarla para envío.
        
        Soporta idempotencia mediante 'idempotency_key'.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Verificar idempotencia
        idempotency_key = serializer.validated_data.get('idempotency_key')
        if idempotency_key:
            existing = NotificationLog.objects.filter(idempotency_key=idempotency_key).first()
            if existing:
                logger.info(f"Duplicate notification with idempotency_key {idempotency_key}")
                return Response(
                    {
                        'id': existing.id,
                        'status': existing.status,
                        'message': 'Notification already exists (idempotent)'
                    },
                    status=status.HTTP_200_OK
                )
        
        # Guardar notificación
        notification = serializer.save()
        
        # Encolar tarea de envío
        try:
            send_notification_task.delay(str(notification.id))
            notification.mark_as_queued()
            logger.info(f"Notification {notification.id} queued for sending")
        except Exception as e:
            logger.error(f"Error queuing notification: {str(e)}")
        
        return Response(
            {
                'id': notification.id,
                'status': 'queued',
                'message': 'Notificación recibida y encolada para envío'
            },
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """
        Estadísticas de notificaciones.
        GET /api/notify/stats/
        """
        total = NotificationLog.objects.count()
        by_type = {}
        for choice in NotificationLog.TYPE_CHOICES:
            type_key = choice[0]
            by_type[type_key] = NotificationLog.objects.filter(notification_type=type_key).count()
        
        by_status = {}
        for choice in NotificationLog.STATUS_CHOICES:
            status_key = choice[0]
            by_status[status_key] = NotificationLog.objects.filter(status=status_key).count()
        
        return Response({
            'total': total,
            'by_type': by_type,
            'by_status': by_status
        })
