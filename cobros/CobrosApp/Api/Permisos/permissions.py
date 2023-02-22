from rest_framework import permissions
from django.contrib.auth.models import User
class AdminSecreatryOrReadOnly(permissions.IsAdminUser):
    def has_permission(self, request, view):
        userName=request.user.username
        user = User.objects.get(username=userName)
        isSecretary=user.groups.filter(name='Secretaria').first()
        isAdmin=user.groups.filter(name='Administrador').first()
        permissioGroup=False
        if isSecretary or isAdmin:
            permissioGroup=True
        return permissioGroup

class AdminOrReadOnlySecretaria(permissions.IsAdminUser):
    def has_permission(self, request, view):
        userName=request.user.username
        user = User.objects.get(username=userName)
        isSecretary=user.groups.filter(name='Secretaria').first()
        permissioGroup=False
        if isSecretary :
            permissioGroup=True
        return permissioGroup

class AdminOrReadOnlyAdmin(permissions.IsAdminUser):
    def has_permission(self, request, view):
        userName=request.user.username
        user = User.objects.get(username=userName)
        isAdmin=user.groups.filter(name='Administrador').first()
        permissioGroup=False
        if isAdmin :
            permissioGroup=True
        return permissioGroup