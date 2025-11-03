from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework import viewsets, mixins
from rest_framework.filters import SearchFilter
from .models import Post
from .serializers import PostListSerializer, PostDetailSerializer


class PostViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    ViewSet para posts del blog.
    
    - List: búsqueda por título/body, paginación
    - Retrieve: detalle cacheado por 120 segundos, incrementa views
    """
    
    queryset = Post.objects.filter(status='published').select_related('author', 'category')
    filter_backends = [SearchFilter]
    search_fields = ['title', 'body']
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PostDetailSerializer
        return PostListSerializer
    
    @method_decorator(cache_page(120))
    def retrieve(self, request, *args, **kwargs):
        """Detalle de post con cache de 120 segundos."""
        response = super().retrieve(request, *args, **kwargs)
        
        # Incrementar views (fuera del cache)
        instance = self.get_object()
        instance.increment_views()
        
        return response
