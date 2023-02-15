import json
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
#from user_app.api.serializers import UserSerializer, UserSerializer
from django.contrib.auth.models import Group
#### PERMISOS ######
#### PERMISOS ######
##from CobrosApp.api.permissions import AdminAuthPutOrReadOnly, AdminOrReadOnly, AuthPermisos
from UserApp import models
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from UserApp.api.serializers import    GroupSerializer, RegistrationSerializer, UserSerializer
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
            isSecretary=user.groups.filter(name='Secretaria').first()
            isAdmin=user.groups.filter(name='Administrador').first()
            isStudent=user.groups.filter(name='Estudiante').first()
        
            if isSecretary |isAdmin:
                return Response({'data':[],'success':False,'message':'No puede acceder a su información desde el móvil'},status=status.HTTP_404_NOT_FOUND)

            if isStudent:
                #user_groups = user.groups.all()
                serializerStudent = GroupSerializer(isStudent, many = True)
                data['Estudiante']=serializerStudent.data
                return Response({'data':data,'success':True,'message':'Inicio de sesión exitosamente'},status=status.HTTP_200_OK)
        elif userAuth == None:
                return Response({'data':data,'success':False,'message':'No existe una cuenta una cuenta'},status=status.HTTP_404_NOT_FOUND)
            
        return Response({'data':data,'success':False,'message':'Contraseña o usuario incorrecto'},status=status.HTTP_404_NOT_FOUND)
 
    except Exception as e:
        return Response({'data':[],'success':False,'message':"ERROR "+str(e)},status=status.HTTP_404_NOT_FOUND)

### OBTENRE USUARIO POR ID Y ACTUALIZAR USUARIO POR ID
@api_view(['GET','PUT','DELETE'])
##@permission_classes([AdminAuthPutOrReadOnly])
def usuario_id_view(request,pk):
    #import pdb; pdb.set_trace()
    try:
        User = get_user_model()
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({'data':[],'success':True,'message':'Usuario no encontrado'},status=status.HTTP_404_NOT_FOUND)

    try:
        if request.method == 'GET':
            serializer =UserSerializer(user)
            return Response({'data':serializer.data,'success':True,'message':'Usuario encontrado'},status=status.HTTP_200_OK)
        
        if request.method=='PUT':
            ## para q no se cree dos veces el mismo objeto
            serializer =UserSerializer(
                data=request.data, instance=user, context={'request': request}
                )
            if serializer.is_valid():
                serializer.save()
                return Response({'data':serializer.data,'success':True,'message':'Usuario actualizado exitosamente'},status=status.HTTP_200_OK)
            else:
               return Response({'data':serializer.errors,'success':False,'message':'No se puede actulizar el usuario'}, status=status.HTTP_400_BAD_REQUEST)

        if request.method=='DELETE':
            serializer = UserSerializer(user)
            user.delete()
            return Response({'data':serializer.data,'success':True,'message':'Usuario elimiado exitosamente'},status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'data':[],'success':False,'message':"ERROR "+str(e)},status=status.HTTP_404_NOT_FOUND)

########## LISTAR TODOS LOS USUARIOS #########
@api_view(['GET'])
#@permission_classes([AdminAuthPutOrReadOnly])
def listar_usuarios_view(request):
    try:
        print(request.user)
        if request.method == 'GET':
            User = get_user_model()
            users = User.objects.all()
            serializer =UserSerializer(users,many=True)
            print(serializer.data)
            return Response({'data':serializer.data,'success':True,'message':'Listado de todos los usuarios'},status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'data':[],'success':False,'message':"ERROR "+str(e)},status=status.HTTP_400_BAD_REQUEST)


########## LISTAR TODOS LOS GRUPOS #########
@api_view(['GET'])
def listar_grupos_view(request):
    try:
        print(request.user)
        if request.method == 'GET':
            groups = Group.objects.all()
            serializer=GroupSerializer(groups,many=True)
            return Response({'data':serializer.data,'success':True,'message':'Listado de todos los usuarios'},status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'data':[],'success':False,'message':"ERROR "+str(e)},status=status.HTTP_400_BAD_REQUEST)

## CERRAR  SESION ######
@api_view(['POST'])
def logout_view(request):
    print("**  CERRAR SESION USER *****")
    print(request)
    try:
        if request.method == 'POST':
            #logout(request)
            request.user.auth_token.delete()
            return Response({'data':[],'success':True,'message':'Sesión cerrada exitosamente'},status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'data':[],'success':False,'message':"ERROR "+str(e)},status=status.HTTP_404_NOT_FOUND)



#### REGISTRAR USUARIO ########
@api_view(['POST'])
#@permission_classes([AdminOrReadOnly])
def registration_view(request):
    try:
        if request.method == 'POST':
            try:
                group = Group.objects.get(name=request.data['group'])
            except  Group.DoesNotExist:
                return Response({'data':[],'success':False,'message':'El grupo '+request.data['group']+"  no existe"},status=status.HTTP_404_NOT_FOUND)
            ##valir que el usuarioname sera unico
            User = get_user_model()
            users_name = User.objects.filter(username=request.data['username']).first()
            if  users_name:
                return Response({'data':[],'success':False,'message':'Ya existe un usurio con el nombre de '+request.data['username']},status=status.HTTP_404_NOT_FOUND)
            users_email = User.objects.filter(email=request.data['email']).first()
            if  users_email:
                return Response({'data':[],'success':False,'message':'Ya existe un usurio con el correo de '+request.data['email']},status=status.HTTP_404_NOT_FOUND)
            
            ## TODO OKKKK
            serializer=RegistrationSerializer(data=request.data)
            data={}
            if not(serializer.is_valid()):
                data=serializer.errors
                return Response({'data':data,'success':False,'message':"No se puede crear el usuario "}, status=status.HTTP_400_BAD_REQUEST)
            
            account=serializer.save()
            data['username']=account.username
            data['email']=account.email
            data['is_staff']=account.is_staff
            token=Token.objects.get(user=account).key
            data['token']=token
            ######### set group #########
            ######### set group #########
            group = Group.objects.get(name=request.data['group'])
            account.groups.add(group)
            serializerGroup=GroupSerializer(group)
            data['grupo']=serializerGroup.data
            return Response({'data':data,'success':True,'message':'Usuario creado exitosamente'},status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error':'ERROR','message':str(e)}, status=status.HTTP_400_BAD_REQUEST)
      