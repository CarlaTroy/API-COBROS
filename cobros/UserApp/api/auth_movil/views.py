import json
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
#from user_app.api.serializers import UserSerializer, UserSerializer
from django.contrib.auth.models import Group
from CobrosApp.Api.CountPassword.views import CountPasswordValidate
from CobrosApp.Api.Student.serializers import StudentSerializer
from CobrosApp.models import Student
#### PERMISOS ######
#### PERMISOS ######
##from CobrosApp.api.permissions import AdminAuthPutOrReadOnly, AdminOrReadOnly, AuthPermisos
from UserApp import models
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from UserApp.api.serializers import    GroupSerializer, UserSerializer, UserSerializer
from django.contrib.auth import authenticate,logout


### INCIAR SESION #####
@api_view(['POST'])
def login_view_movil(request):
    try:
        data={}
        #import pdb; pdb.set_trace()
        #recuperamos las credenciales y autenticamos al usuarios
        usuarioName=request.data.get('username',None)
        password=request.data.get('password',None)
        ## ======== validar numero de intentos de contraseña =========##
        user = User.objects.get(username=usuarioName)
        response=(CountPasswordValidate.intent(user,password))
        if response:
           return Response(response,status=status.HTTP_404_NOT_FOUND)
        userAuth=authenticate(username=usuarioName, password=password)
        ## si es correcto añadirmos a la reques la ifnroamcion de sesion
        if userAuth:
            #User = get_user_model()
            user = User.objects.get(username=usuarioName)
            data['id']=user.id
            data['username']=user.username
            data['email']=user.email
            data['is_staff']=user.is_staff
            token, _ = Token.objects.get_or_create(user=userAuth)
            data['token']=token.key,
            ##grupo que pertenece
            user_groups = user.groups.all()
            isSecretary=user.groups.filter(name='Secretaria').first()
            isAdmin=user.groups.filter(name='Administrador').first()
            isStudent=user.groups.filter(name='Estudiante').first()
        
            if isSecretary or isAdmin:
                return Response({'data':[],'success':False,'message':'No puede acceder a su información desde el móvil'},status=status.HTTP_404_NOT_FOUND)

            if isStudent:
                #user_groups = user.groups.all()
                serializerGroups = GroupSerializer(user_groups, many = True)
                student=Student.objects.get(user__pk=user.id)
                #serializerStudent = StudentSerializer(student, many = True)
                estudianteGruop={
                    "id": student.id,
                    "name": serializerGroups.data[0]['name'],
                    "permissions": serializerGroups.data[0]['permissions']
                }
                grupoEstudiante=[estudianteGruop]
                data['grupos']=grupoEstudiante
                return Response({'data':data,'success':True,'message':'Inicio de sesión exitosamente'},status=status.HTTP_200_OK)
        elif userAuth == None:
                return Response({'data':data,'success':False,'message':'No existe una cuenta una cuenta'},status=status.HTTP_404_NOT_FOUND)
            
        return Response({'data':data,'success':False,'message':'Contraseña o usuario incorrecto'},status=status.HTTP_404_NOT_FOUND)
 
    except Exception as e:
        return Response({'data':[],'success':False,'message':"ERROR "+str(e)},status=status.HTTP_404_NOT_FOUND)

#