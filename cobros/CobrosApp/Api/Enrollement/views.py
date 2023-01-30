from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from CobrosApp.Api.Enrollement.serializers import EnrollementSerializer
from CobrosApp.Api.Payment.serializers import PaymentSerializer
from CobrosApp.models import Enrollement, Status_Pay,Cohorte
from datetime import date, datetime

class EnrollementAV(APIView):
    def get(self, request):
        data=None
        try:
            enrollement=Enrollement.objects.all()
            serializer=EnrollementSerializer(enrollement,many=True)
            data=serializer.data
            return Response({'data':data,'success':True,'message':'Listado de las matriculas'},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'data':data,'success':False,'message':'Error '+str(e)},status=status.HTTP_404_NOT_FOUND)
    def post(self,request):
        #import pdb; pdb.set_trace()
        data=None
        try:
            serializer=EnrollementSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                #import pdb; pdb.set_trace()
                data=serializer.data
                ## CODIGO 001 ES EN CUOTAS
                #una vez creada la matricula vemos los pagos creamos una tabla de pagos si en algn caso tiene credito
                if data['tipe_pay']['codigo']=='001':
                    ##obtener el estado de pago de la tabla estado de pago
                    idStatusPay=Status_Pay.objects.filter(codigo='002').first()
                    ##definir fechas de pagos
                    now = date.today()
                    ##recorrer para el numero de cuotas
                    count=1
                    arrayPayment=list()
                    #import pdb; pdb.set_trace()
                    cohorte=Cohorte.objects.filter(pk=request.data['cohorte_id']).first()
                    cuotas=int(request.data['cuotas'])
                    descuentoCosuto=int(cohorte.cost_credit)-(int(cohorte.cost_credit)*(request.data['discount']/100))
                    amount=(descuentoCosuto/cuotas)
                    while count<=data['cuotas']:
                        next_month = datetime(now.year, now.month+(count),data['day_limite'])
                        dataPayment={
                            "amount": float("%3.f" % amount),
                            "date_pay": next_month.date(),
                            "date_limit": next_month.date(),
                            "status_pay_id": idStatusPay.id,
                            "enrollement_id":data['id']
                        }
                        serializerPayment=PaymentSerializer(data=dataPayment)
                        if serializerPayment.is_valid():
                            serializerPayment.save()
                            arrayPayment.append(serializerPayment.data)
                            count=count+1
                        else:
                            return Response({'data':serializerPayment.errors,'success':False,'message':'No se puede crear los pagos de creditos'}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        dataMatriculaPago={
                            "enrollement":data,
                            "payment":arrayPayment
                        }    
                        return Response({'data':dataMatriculaPago,'success':True,'message':'Matricula  y Pagos creado exitosamente'},status=status.HTTP_201_CREATED)
                return Response({'data':data,'success':True,'message':'Matriculas creado exitosamente'},status=status.HTTP_201_CREATED)
            else:
                return Response({'data':serializer.errors,'success':False,'message':'No se puede crear la matricula'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'data':data,'success':False,'message':'Error '+str(e)},status=status.HTTP_404_NOT_FOUND)
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