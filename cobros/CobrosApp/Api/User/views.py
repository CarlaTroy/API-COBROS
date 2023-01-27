from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from CobrosApp.Api.Cohorte.serializers import CohorteSerializer 
from CobrosApp.models import Cohorte
from cobros.CobrosApp.Api.Student.serializers import StudentSerializer

class StudentAV(APIView):
    def get(self, request):
        data=None
        try:
            courses=StudentSerializer.all()
            serializer=CohorteSerializer(courses,many=True)
            data=serializer.data
            return Response({'data':data,'success':True,'message':'Listado de cohortes'},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'data':data,'success':False,'message':'Error '+str(e)},status=status.HTTP_404_NOT_FOUND)
    def post(self,request):
        data=None
        try:
            serializer=CohorteSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                data=serializer.data
                return Response({'data':data,'success':True,'message':'Cohorte creado exitosamente'},status=status.HTTP_201_CREATED)
            else:
                return Response({'data':serializer.errors,'success':False,'message':'No se puede crear la cohorte'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'data':data,'success':False,'message':'Error '+str(e)},status=status.HTTP_404_NOT_FOUND)
class CohorteDetail(APIView):
    def get(self,request,pk):
        data=None
        #buscar el registro
        try:
            course=Cohorte.objects.get(pk=pk)
            serializer=CohorteSerializer(course)
            data=serializer.data
            return Response({'data':data,'success':True,'message':'Cohorte encontrada'},status=status.HTTP_200_OK)
        except course.DoesNotExist :
            return Response({'data':data,'success':False,'message':'Cohorte no encontrado'},status=status.HTTP_404_NOT_FOUND)
    
    def put(self,request,pk):
        data=None
        course=None
        try:
            course=Cohorte.objects.get(pk=pk)
            serializer=CohorteSerializer(course,data=request.data)
            if serializer.is_valid():
                serializer.save()
                data=serializer.data
                return Response({'data':data,'success':True,'message':'Cohorte actualizado'},status=status.HTTP_200_OK)
            else:
                return Response({'data':serializer.errors,'success':False,'message':'No se puede actulizar el Cohorte'}, status=status.HTTP_400_BAD_REQUEST)
        except Cohorte.DoesNotExist:
            return Response({'data':data,'success':False,'message':'Cohorte no encontrado'},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'data':serializer.errors,'success':False,'message':"ERROR "+str(e)}, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk):
        data=None
        course=None
        try:
            course=Cohorte.objects.get(pk=pk)
            course.delete()
            return Response({'data':[],'success':True,'message':'Cohorte eliminado'},status=status.HTTP_200_OK)
        except Cohorte.DoesNotExist:
            return Response({'data':data,'success':False,'message':'Cohorte no encontrado'},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'data':data,'success':False,'message':"ERROR "+str(e)}, status=status.HTTP_400_BAD_REQUEST)