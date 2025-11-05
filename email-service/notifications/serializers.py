"""
Serializers para la app de notificaciones.
"""
from rest_framework import serializers
from .models import ContactMessage, NotificationLog


class ContactMessageSerializer(serializers.ModelSerializer):
    """
    Serializer para mensajes de contacto.
    """
    class Meta:
        model = ContactMessage
        fields = ['id', 'name', 'email', 'message', 'status', 'created_at']
        read_only_fields = ['id', 'status', 'created_at']
    
    def validate_name(self, value):
        """Valida que el nombre no esté vacío."""
        if not value or not value.strip():
            raise serializers.ValidationError("El nombre no puede estar vacío")
        return value.strip()
    
    def validate_message(self, value):
        """Valida que el mensaje tenga al menos 10 caracteres."""
        if len(value.strip()) < 10:
            raise serializers.ValidationError("El mensaje debe tener al menos 10 caracteres")
        return value.strip()


class ContactMessageListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listado de mensajes de contacto.
    """
    class Meta:
        model = ContactMessage
        fields = ['id', 'name', 'email', 'status', 'created_at']


class NotificationSerializer(serializers.ModelSerializer):
    """
    Serializer para notificaciones (endpoint interno).
    """
    class Meta:
        model = NotificationLog
        fields = ['id', 'notification_type', 'to', 'subject', 'body', 'status', 
                  'source_service', 'idempotency_key', 'created_at']
        read_only_fields = ['id', 'status', 'created_at']
    
    def validate_to(self, value):
        """Valida que el email de destino sea válido."""
        if not value or not value.strip():
            raise serializers.ValidationError("El email de destino es requerido")
        return value.strip()
    
    def validate_body(self, value):
        """Valida que el cuerpo del mensaje no esté vacío."""
        if not value or not value.strip():
            raise serializers.ValidationError("El cuerpo del mensaje no puede estar vacío")
        return value.strip()


class NotificationListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listado de notificaciones.
    """
    class Meta:
        model = NotificationLog
        fields = ['id', 'notification_type', 'to', 'subject', 'status', 'source_service', 'created_at']
