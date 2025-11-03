from django.db import models


class Author(models.Model):
    """
    Modelo de Author para los posts del blog.
    Por ahora es local (seed data).
    En el Día 4 se enlazará con el Auth Service.
    """
    
    display_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['display_name']
    
    def __str__(self):
        return self.display_name
