from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from CobrosApp.Api.Enrollement.serializers import EnrollementSerializer
from CobrosApp.Api.Payment.serializers import PaymentSerializer
from CobrosApp.models import Enrollement, Payment

class PaymentAV(APIView):
    def get(self, request):
        data=None
        try:
            enrollement=Payment.objects.all()
            serializer=PaymentSerializer(enrollement,many=True)
            data=serializer.data
            return Response({'data':data,'success':True,'message':'Listado de los pagos'},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'data':data,'success':False,'message':'Error '+str(e)},status=status.HTTP_404_NOT_FOUND)
    def post(self,request):
        #import pdb; pdb.set_trace()
        data=None
        try:
            serializer=EnrollementSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                data=serializer.data
                return Response({'data':data,'success':True,'message':'Matricula  creado exitosamente'},status=status.HTTP_201_CREATED)
            else:
                return Response({'data':serializer.errors,'success':False,'message':'No se puede actualizar la matricula'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'data':data,'success':False,'message':'Error '+str(e)},status=status.HTTP_404_NOT_FOUND)
class PaymentDetail(APIView):
    def get(self,request,pk):
        data=None
        #buscar el registro
        try:
            payment=Payment.objects.get(pk=pk)
            serializer=PaymentSerializer(payment)
            data=serializer.data
            return Response({'data':data,'success':True,'message':'Pago encontrada'},status=status.HTTP_200_OK)
        except Enrollement.DoesNotExist :
            return Response({'data':data,'success':False,'message':'Pago no encontrado'},status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk):
        data=None
        course=None
        try:
            course=Enrollement.objects.get(pk=pk)
            course.delete()
            return Response({'data':[],'success':True,'message':'Matricula eliminado'},status=status.HTTP_200_OK)
        except Enrollement.DoesNotExist:
            return Response({'data':data,'success':False,'message':'Matricula no encontrado'},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'data':data,'success':False,'message':"ERROR "+str(e)}, status=status.HTTP_400_BAD_REQUEST)