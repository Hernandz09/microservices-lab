from django.db import models
from slugify import slugify
from categories.models import Category
from authors.models import Author


class Post(models.Model):
    """Modelo de Post para el blog."""
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    body = models.TextField()
    excerpt = models.TextField(max_length=500, blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='posts')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    views = models.PositiveIntegerField(default=0)
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-published_at', '-created_at']
        indexes = [
            models.Index(fields=['status', '-published_at']),
            models.Index(fields=['slug']),
        ]
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        
        # Generar excerpt si no existe
        if not self.excerpt and self.body:
            self.excerpt = self.body[:200] + ('...' if len(self.body) > 200 else '')
        
        super().save(*args, **kwargs)
    
    def increment_views(self):
        """Incrementa el contador de vistas."""
        self.views += 1
        self.save(update_fields=['views'])
