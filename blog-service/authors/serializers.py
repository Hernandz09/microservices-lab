from rest_framework import serializers
from .models import Author


class AuthorSerializer(serializers.ModelSerializer):
    """Serializer para Author."""
    
    class Meta:
        model = Author
        fields = ['id', 'display_name', 'email']
