from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    """Serializer para Category."""
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']
