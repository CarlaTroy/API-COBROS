from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from CobrosApp.models import Course
from CobrosApp.Api.Course.serializers import CouserSerializer

class CourseAV(APIView):
    def get(self, request):
        data=None
        try:
            courses=Course.objects.all()
            serializer=CouserSerializer(courses,many=True)
            data=serializer.data
            return Response({'data':data,'succes':True,'message':'Listado de cursos'},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'data':data,'succes':False,'message':'Error '+str(e)},status=status.HTTP_404_NOT_FOUND)
    def post(self,request):
        data=None
        try:
            serializer=CouserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                data=serializer.data
                return Response({'data':data,'succes':True,'message':'Curso creado exitosamente'},status=status.HTTP_200_OK)
            else:
                return Response({'data':serializer.errors,'success':False,'message':'No se puede crear el curso'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'data':data,'succes':False,'message':'Error '+str(e)},status=status.HTTP_404_NOT_FOUND)