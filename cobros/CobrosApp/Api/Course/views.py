from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from CobrosApp.models import Course
from CobrosApp.Api.Course.serializers import CouserSerializer
from rest_framework.permissions import BasePermission, DjangoModelPermissions
class CourseAV(APIView):
    permission_classes = [DjangoModelPermissions]
    group_required = ['Administrador']
    def get(self, request):
        data=None
        try:
            courses=Course.objects.all()
            serializer=CouserSerializer(courses,many=True)
            data=serializer.data
            return Response({'data':data,'success':True,'message':'Listado de cursos'},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'data':data,'success':False,'message':'Error '+str(e)},status=status.HTTP_404_NOT_FOUND)
    def post(self,request):
        data=None
        try:
            serializer=CouserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                data=serializer.data
                return Response({'data':data,'success':True,'message':'Curso creado exitosamente'},status=status.HTTP_201_CREATED)
            else:
                return Response({'data':serializer.errors,'success':False,'message':'No se puede crear el curso'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'data':data,'success':False,'message':'Error '+str(e)},status=status.HTTP_404_NOT_FOUND)
class CourseDetail(APIView):
    def get(self,request,pk):
        data=None
        #buscar el registro
        try:
            course=Course.objects.get(pk=pk)
            serializer=CouserSerializer(course)
            data=serializer.data
            return Response({'data':data,'success':True,'message':'Curso encontrada'},status=status.HTTP_200_OK)
        except course.DoesNotExist :
            return Response({'data':data,'success':False,'message':'Curso no encontrado'},status=status.HTTP_404_NOT_FOUND)
    
    def put(self,request,pk):
        data=None
        course=None
        try:
            course=Course.objects.get(pk=pk)
            serializer=CouserSerializer(course,data=request.data)
            if serializer.is_valid():
                serializer.save()
                data=serializer.data
                return Response({'data':data,'success':True,'message':'Curso actualizado'},status=status.HTTP_200_OK)
            else:
                return Response({'data':serializer.errors,'success':False,'message':'No se puede actulizar el curso'}, status=status.HTTP_400_BAD_REQUEST)
        except Course.DoesNotExist:
            return Response({'data':data,'success':False,'message':'Curso no encontrado'},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'data':serializer.errors,'success':False,'message':"ERROR "+str(e)}, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk):
        data=None
        course=None
        try:
            course=Course.objects.get(pk=pk)
            course.delete()
            return Response({'data':[],'success':True,'message':'Curso eliminado'},status=status.HTTP_200_OK)
        except Course.DoesNotExist:
            return Response({'data':data,'success':False,'message':'Curso no encontrado'},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'data':data,'success':False,'message':"ERROR "+str(e)}, status=status.HTTP_400_BAD_REQUEST)