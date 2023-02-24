import json
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
#from user_app.api.serializers import UserSerializer, UserSerializer
from django.contrib.auth.models import Group
from CobrosApp.Api.CountPassword.views import CountPasswordValidate
#### PERMISOS ######
#### PERMISOS ######
from CobrosApp.Api.Permisos.permissions import AdminOrReadOnlyAdmin, AdminSecreatryOrReadOnly, AdminOrReadOnlySecretaria
from UserApp import models
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from UserApp.api.serializers import    GroupSerializer, UserSerializer, UserSerializer
from django.contrib.auth import authenticate,logout

#validatePasswordCount=list()
#cache.set('demo', validatePasswordCount, timeout=None)
### INCIAR SESION #####
@api_view(['POST'])
def login_view(request):
    try:
        data={}
        #import pdb; pdb.set_trace()
        #recuperamos las credenciales y autenticamos al usuarios
        usuarioName=request.data.get('username',None)
        password=request.data.get('password',None)
        
        ######  verificar si la contraseña es incorrecta  ########
        #cont=0
        user = User.objects.get(username=usuarioName)
        ## ======== validar numero de intentos de contraseña =========##
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
            existGrupo = False
            isStudent=user.groups.filter(name='Estudiante').first()
            isSecretary=user.groups.filter(name='Secretaria').first()
            isAdmin=user.groups.filter(name='Administrador').first()

            if isStudent:
                existGrupo=True
                return Response({'data':[],'success':False,'message':'No puede acceder a su información desde la web debe hacer mediante la app como estudiante'},status=status.HTTP_404_NOT_FOUND)
            
            if isSecretary or isAdmin:
                existGrupo=True
                user_groups = user.groups.all()
                serializerGroups=GroupSerializer(user_groups,many=True)
                data['grupos']=serializerGroups.data
                return Response({'data':data,'success':True,'message':'Inicio de sesión exitosamente'},status=status.HTTP_200_OK)
            if not existGrupo:
                return Response({'data':[],'success':False,'message':'El usuario no pertenece a ningun grupo'},status=status.HTTP_404_NOT_FOUND)
        elif userAuth == None:
            return Response({'data':[],'success':False,'message':'No existe una cuenta una cuenta con este usuario'},status=status.HTTP_404_NOT_FOUND)
            
        return Response({'data':[],'success':False,'message':'Contraseña o usuario incorrecto'},status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'data':[],'success':False,'message':"ERROR "+str(e)},status=status.HTTP_404_NOT_FOUND)

### OBTENRE USUARIO POR ID Y ACTUALIZAR USUARIO POR ID
@api_view(['GET','PUT','DELETE'])
@permission_classes([AdminOrReadOnlyAdmin])
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
            serializerActualizar =UserSerializer(user,data=request.data)
            dataUser={
                'username':request.data['username'],
                'email':request.data['email'],
                'password':request.data['password'],
                'password2':request.data['password2'],
                'is_staff':request.data['is_staff'],
                'is_active':request.data['is_active'],
            }
            if serializerActualizar.is_valid():
                serializerActualizar.update(user,dataUser)
                
                user.groups.clear()
                grupo = Group.objects.get(name=request.data['group'])
                grupo.user_set.add(user)
                grupo.save()
                return Response({'data':serializerActualizar.data,'success':True,'message':'Usuario actualizado exitosamente'},status=status.HTTP_200_OK)
            else:
               return Response({'data':serializerActualizar.errors,'success':False,'message':'No se puede actulizar el usuario'}, status=status.HTTP_400_BAD_REQUEST)

        if request.method=='DELETE':
            serializer = UserSerializer(user)
            user.delete()
            return Response({'data':serializer.data,'success':True,'message':'Usuario elimiado exitosamente'},status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'data':[],'success':False,'message':"ERROR "+str(e)},status=status.HTTP_404_NOT_FOUND)

########## LISTAR TODOS LOS USUARIOS #########
@api_view(['GET'])
@permission_classes([AdminOrReadOnlyAdmin])
def listar_usuarios_view(request):
    try:
        if request.method == 'GET':
            #users_with_groups = User.objects.prefetch_related('Adminstrador').all()
            User = get_user_model()
            users = User.objects.prefetch_related('groups').all()
            serializer =UserSerializer(users,many=True)
            print(serializer.data)
            return Response({'data':serializer.data,'success':True,'message':'Listado de todos los usuarios'},status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'data':[],'success':False,'message':"ERROR "+str(e)},status=status.HTTP_400_BAD_REQUEST)


########## LISTAR TODOS LOS GRUPOS #########
@api_view(['GET'])
@permission_classes([AdminOrReadOnlyAdmin])
def listar_grupos_view(request):
    try:
        if request.method == 'GET':
            groups = Group.objects.all()
            serializer=GroupSerializer(groups,many=True)
            return Response({'data':serializer.data,'success':True,'message':'Listado de todos los usuarios'},status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'data':[],'success':False,'message':"ERROR "+str(e)},status=status.HTTP_400_BAD_REQUEST)

## CERRAR  SESION ######
@api_view(['POST'])
def logout_view(request):
    try:
        if request.method == 'POST':
            #logout(request)
            request.user.auth_token.delete()
            return Response({'data':[],'success':True,'message':'Sesión cerrada exitosamente'},status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'data':[],'success':False,'message':"ERROR "+str(e)},status=status.HTTP_404_NOT_FOUND)



#### REGISTRAR USUARIO ########
@api_view(['POST'])
@permission_classes([AdminOrReadOnlyAdmin])
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
            serializer=UserSerializer(data=request.data)
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
      