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
class StudentOrReadOnly(permissions.IsAdminUser):
    def has_permission(self, request, view):
        userName=request.user.username
        user = User.objects.get(username=userName)
        isEstudiante=user.groups.filter(name='Estudiante').first()
        permissioGroup=False
        if isEstudiante :
            permissioGroup=True
        return permissioGroup

    
class StudentAdminPutOrReadOnly(permissions.IsAdminUser):
     def has_permission(self, request, view):
        userName=request.user.username
        user = User.objects.get(username=userName)
        isStudent=user.groups.filter(name='Estudiante').first()
        isAdmin=user.groups.filter(name='Administrador').first()
        permissioGroup=False
        if request.method =='PUT'and  isStudent:
            permissioGroup=True
        if isAdmin:
            permissioGroup=True
        return permissioGroup
    

class SecrataryAdminPutOrReadOnly(permissions.IsAdminUser):
     def has_permission(self, request, view):
        userName=request.user.username
        user = User.objects.get(username=userName)
        isSecretaria=user.groups.filter(name='Secretaria').first()
        isAdmin=user.groups.filter(name='Administrador').first()
        permissioGroup=False
        if request.method =='PUT'and  isSecretaria:
            permissioGroup=True
        if isAdmin:
            permissioGroup=True
        return permissioGroup