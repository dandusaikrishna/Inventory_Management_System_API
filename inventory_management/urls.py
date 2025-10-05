"""inventory_management URL Configuration"""
from django.urls import path, include

urlpatterns = [
    path('api/v1/', include('inventory.urls')),
]
