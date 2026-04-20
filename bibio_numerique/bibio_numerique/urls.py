from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/auth/', include('comptes.urls')),
    path('api/', include('gestion.urls')),
]