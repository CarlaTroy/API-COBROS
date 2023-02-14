from django.contrib.auth.models import Group
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from CobrosApp.models import Student
from CobrosApp.Api.Student.serializers import StudentSerializer
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from UserApp.api.auth_web.serializers import GroupSerializer, RegistrationSerializer
class StudentAV(APIView):
    def get(self, request):
        data=None
        try:
            students=Student.objects.all()
            serializer=StudentSerializer(students,many=True)
            data=serializer.data
            return Response({'data':data,'success':True,'message':'Listado de estudiantes'},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'data':data,'success':False,'message':'Error '+str(e)},status=status.HTTP_404_NOT_FOUND)
    def post(self,request):
        #import pdb; pdb.set_trace()
        data=None
        group:None
        ##buscar el grupo estudiante
        try:
            group = Group.objects.get(name='Estudiante')
        except Group.DoesNotExist:
            return Response({'data':[],'success':False,'message':"El grupo no existe"},status=status.HTTP_404_NOT_FOUND)
        try:
            ##buscamos el usuario
            User = get_user_model()
            users_name = User.objects.filter(username=request.data['identification']).first()
            if  users_name:
                return Response({'data':[],'success':False,'message':'Ya existe un usurio con la identificación '+request.data['identification']},status=status.HTTP_400_BAD_REQUEST)
            
            users_email = User.objects.filter(email=request.data['email']).first()
            if  users_email:
                return Response({'data':[],'success':False,'message':'Ya existe un usurio con el correo de '+request.data['email']},status=status.HTTP_400_BAD_REQUEST)
            
            ##registrar usuario y esutdiante
            dataUser={
                'username':request.data['identification'],
                'email':request.data['email'],
                'password':request.data['identification'],
                'password2':request.data['identification'],
                'is_staff':True,
            }
            serialzerUsuario=RegistrationSerializer(data=dataUser)
            if not (serialzerUsuario.is_valid()):
                return Response({'data':serialzerUsuario.errors,'success':False,'message':'No se puede crear el usuario'}, status=status.HTTP_400_BAD_REQUEST)
            
            ##SE CREA EL USUARIO TODO OK
            usuario=serialzerUsuario.save()
            #ASIGNAR A UN GRUPO
            usuario.groups.add(group)
            serializerGroup=GroupSerializer(group)
            
            ## CREAR EL ESTUDIANTE
            dataEstudiante={
                'name':request.data['name'],
                'last_name':request.data['last_name'],
                'identification':request.data['identification'],
                'address':request.data['address'],
                'cell_phone':request.data['cell_phone'],
                'user_id':usuario.id
            }
            serializerStudent=StudentSerializer(data=dataEstudiante)
            
            if not (serializerStudent.is_valid()):
                return Response({'data':serializerStudent.errors,'success':False,'message':'No se puede crear el estudiante'}, status=status.HTTP_400_BAD_REQUEST)
            serializerStudent.save()
            data={
                'user':serialzerUsuario.data,
                'student':serializerStudent.data,
                'group':serializerGroup.data
            }
            return Response({'data':data,'success':True,'message':'Estudiante creado exitosamente'},status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'data':data,'success':False,'message':'Error '+str(e)},status=status.HTTP_404_NOT_FOUND)

class StudentDetail(APIView):
    def get(self,request,pk):
        data=None
        #buscar el registro
        try:
            estudiante=Student.objects.get(pk=pk)
            serializer=StudentSerializer(estudiante)
            data=serializer.data
            return Response({'data':data,'success':True,'message':'Estudiante encontrada'},status=status.HTTP_200_OK)
        except Student.DoesNotExist :
            return Response({'data':data,'success':False,'message':'Estudiante no encontrado'},status=status.HTTP_404_NOT_FOUND)
    
    def put(self,request,pk):
        data=None
        estudiante=None
        try:
            estudiante=Student.objects.get(pk=pk)
            serializer=StudentSerializer(estudiante,data=request.data)
            if serializer.is_valid():
                serializer.save()
                data=serializer.data
                return Response({'data':data,'success':True,'message':'Cohorte actualizado'},status=status.HTTP_200_OK)
            else:
                return Response({'data':serializer.errors,'success':False,'message':'No se puede actulizar el Cohorte'}, status=status.HTTP_400_BAD_REQUEST)
        except Student.DoesNotExist:
            return Response({'data':data,'success':False,'message':'Cohorte no encontrado'},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'data':serializer.errors,'success':False,'message':"ERROR "+str(e)}, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk):
        data=None
        course=None
        try:
            course=Student.objects.get(pk=pk)
            course.delete()
            return Response({'data':[],'success':True,'message':'Estudiante eliminado'},status=status.HTTP_200_OK)
        except Student.DoesNotExist:
            return Response({'data':data,'success':False,'message':'Estudiante no encontrado'},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'data':data,'success':False,'message':"ERROR "+str(e)}, status=status.HTTP_400_BAD_REQUEST)