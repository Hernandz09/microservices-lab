"""
URL configuration for notifications app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContactMessageViewSet, NotificationViewSet

router = DefaultRouter()
router.register(r'contact', ContactMessageViewSet, basename='contact')
router.register(r'notify', NotificationViewSet, basename='notify')

urlpatterns = [
    path('', include(router.urls)),
]
