from rest_framework import serializers
from .models import Post
from categories.serializers import CategorySerializer
from authors.serializers import AuthorSerializer


class PostListSerializer(serializers.ModelSerializer):
    """Serializer para lista de posts."""
    
    author = AuthorSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    
    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'slug',
            'excerpt',
            'author',
            'category',
            'published_at',
            'views'
        ]


class PostDetailSerializer(serializers.ModelSerializer):
    """Serializer para detalle de post."""
    
    author = AuthorSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    
    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'slug',
            'body',
            'excerpt',
            'author',
            'category',
            'status',
            'published_at',
            'views',
            'created_at',
            'updated_at'
        ]
