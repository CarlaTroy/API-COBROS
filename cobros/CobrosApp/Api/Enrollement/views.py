from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from CobrosApp.Api.Enrollement.serializers import EnrollementSerializer
from CobrosApp.Api.Payment.serializers import PaymentSerializer
from CobrosApp.models import Enrollement

class EnrollementAV(APIView):
    def get(self, request):
        data=None
        try:
            enrollement=Enrollement.objects.all()
            serializer=EnrollementSerializer(enrollement,many=True)
            data=serializer.data
            return Response({'data':data,'succes':True,'message':'Listado de las matriculas'},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'data':data,'succes':False,'message':'Error '+str(e)},status=status.HTTP_404_NOT_FOUND)
    def post(self,request):
        #import pdb; pdb.set_trace()
        data=None
        try:
            serializer=EnrollementSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                data=serializer.data
                ## CODIGO 001 ES EN CUOTAS
                #una vez creada la matricula vemos los pagos creamos una tabla de pagos si en algn caso tiene credito
                """                 if data.tipe_pay.codigo=='001':
                                    dataPayment={
                                        "amount": 0,
                                        "date_pay": None,
                                        "date_limit": None,
                                        "status_pay": None,
                                        "cuotas":data.cuotas,
                                        "enrollement_id":data.day_limite,
                                    }
                                    serializerPayment=PaymentSerializer(data=data) """
                return Response({'data':data,'succes':True,'message':'Matricula  creado exitosamente'},status=status.HTTP_201_CREATED)
            else:
                return Response({'data':serializer.errors,'success':False,'message':'No se puede actualizar la matricula'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'data':data,'succes':False,'message':'Error '+str(e)},status=status.HTTP_404_NOT_FOUND)
class EnrollementDetail(APIView):
    def get(self,request,pk):
        data=None
        #buscar el registro
        try:
            enrollement=Enrollement.objects.get(pk=pk)
            serializer=EnrollementSerializer(enrollement)
            data=serializer.data
            return Response({'data':data,'success':True,'message':'Matricula encontrada'},status=status.HTTP_200_OK)
        except Enrollement.DoesNotExist :
            return Response({'data':data,'success':False,'message':'Matricula no encontrado'},status=status.HTTP_404_NOT_FOUND)
    
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