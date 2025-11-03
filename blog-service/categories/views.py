from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework import viewsets, mixins
from .models import Category
from .serializers import CategorySerializer


@method_decorator(cache_page(60), name='list')
class CategoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    ViewSet para listar categorías activas.
    La lista está cacheada por 60 segundos.
    """
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
