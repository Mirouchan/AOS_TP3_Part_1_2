from rest_framework.permissions import BasePermission

class IsBibliothecaire(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.groups.filter(name='Bibliothecaire').exists()
        )
    
class IsLecteur(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.groups.filter(name='Lecteur').exists()
        )


