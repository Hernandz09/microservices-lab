from django.contrib import admin
from .models import ContactMessage, NotificationLog


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'status', 'created_at', 'processed_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'email', 'message']
    readonly_fields = ['id', 'created_at', 'updated_at', 'processed_at']
    ordering = ['-created_at']


@admin.register(NotificationLog)
class NotificationLogAdmin(admin.ModelAdmin):
    list_display = ['to', 'subject', 'notification_type', 'status', 'source_service', 'created_at']
    list_filter = ['notification_type', 'status', 'created_at']
    search_fields = ['to', 'subject', 'body', 'source_service']
    readonly_fields = ['id', 'created_at', 'updated_at', 'sent_at']
    ordering = ['-created_at']
