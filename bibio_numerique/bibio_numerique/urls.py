from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('gestion.urls')),
    path('', include('UI_bibliotheque.urls')),
    path('comptes/', include('comptes.urls')),
]