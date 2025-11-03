from django.contrib import admin
from .models import Author


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['display_name', 'email', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['display_name', 'email']
