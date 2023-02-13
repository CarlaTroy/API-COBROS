from email.headerregistry import Group
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from CobrosApp.models import Student
from CobrosApp.Api.Student.serializers import StudentSerializer
from django.contrib.auth.models import User
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
        try:
            serializer=StudentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                ##asinar a un grupo
                data=serializer.data
                
                return Response({'data':data,'success':True,'message':'Estudiante creado exitosamente'},status=status.HTTP_201_CREATED)
            else:
                return Response({'data':serializer.errors,'success':False,'message':'No se puede crear el estudiante'}, status=status.HTTP_400_BAD_REQUEST)
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