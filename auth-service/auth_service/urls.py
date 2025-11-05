"""
URL Configuration for auth_service project.
"""
from django.contrib import admin
from django.urls import path, include
from users.healthcheck import healthcheck

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('healthz', healthcheck, name='healthcheck'),
]
