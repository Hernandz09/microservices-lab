"""
Modelos para el servicio de notificaciones.
"""
from django.db import models
from django.utils import timezone
import uuid


class ContactMessage(models.Model):
    """
    Mensajes de contacto recibidos desde formularios.
    """
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('queued', 'En Cola'),
        ('sent', 'Enviado'),
        ('failed', 'Fallido'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, help_text="Nombre del remitente")
    email = models.EmailField(help_text="Email del remitente")
    message = models.TextField(help_text="Mensaje del contacto")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    
    # Retry tracking
    retry_count = models.PositiveIntegerField(default=0)
    last_error = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['email']),
        ]
        verbose_name = 'Mensaje de Contacto'
        verbose_name_plural = 'Mensajes de Contacto'
    
    def __str__(self):
        return f"{self.name} ({self.email}) - {self.status}"
    
    def mark_as_queued(self):
        """Marca el mensaje como encolado."""
        self.status = 'queued'
        self.save(update_fields=['status', 'updated_at'])
    
    def mark_as_sent(self):
        """Marca el mensaje como enviado."""
        self.status = 'sent'
        self.processed_at = timezone.now()
        self.save(update_fields=['status', 'processed_at', 'updated_at'])
    
    def mark_as_failed(self, error_message):
        """Marca el mensaje como fallido."""
        self.status = 'failed'
        self.last_error = error_message
        self.retry_count += 1
        self.processed_at = timezone.now()
        self.save(update_fields=['status', 'last_error', 'retry_count', 'processed_at', 'updated_at'])


class NotificationLog(models.Model):
    """
    Log de todas las notificaciones enviadas (desde otros servicios).
    """
    TYPE_CHOICES = [
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('push', 'Push Notification'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('queued', 'En Cola'),
        ('sent', 'Enviado'),
        ('failed', 'Fallido'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='email')
    
    # Destinatario
    to = models.EmailField(help_text="Destinatario")
    subject = models.CharField(max_length=500, blank=True)
    body = models.TextField()
    
    # Estado
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Metadata
    source_service = models.CharField(max_length=100, blank=True, help_text="Servicio que solicitó la notificación")
    idempotency_key = models.CharField(max_length=255, unique=True, null=True, blank=True, 
                                       help_text="Clave de idempotencia para evitar duplicados")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    
    # Retry tracking
    retry_count = models.PositiveIntegerField(default=0)
    last_error = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['to']),
            models.Index(fields=['idempotency_key']),
        ]
        verbose_name = 'Log de Notificación'
        verbose_name_plural = 'Logs de Notificaciones'
    
    def __str__(self):
        return f"{self.notification_type.upper()} to {self.to} - {self.status}"
    
    def mark_as_queued(self):
        """Marca la notificación como encolada."""
        self.status = 'queued'
        self.save(update_fields=['status', 'updated_at'])
    
    def mark_as_sent(self):
        """Marca la notificación como enviada."""
        self.status = 'sent'
        self.sent_at = timezone.now()
        self.save(update_fields=['status', 'sent_at', 'updated_at'])
    
    def mark_as_failed(self, error_message):
        """Marca la notificación como fallida."""
        self.status = 'failed'
        self.last_error = error_message
        self.retry_count += 1
        self.save(update_fields=['status', 'last_error', 'retry_count', 'updated_at'])
