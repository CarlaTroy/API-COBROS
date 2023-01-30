from CobrosApp.Api.Status_Pay.serializers import StatusPaySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from CobrosApp.models import Status_Pay
class TypePayseAV(APIView):
    def get(self, request):
        data=None
        try:
            statusPay=Status_Pay.objects.all()
            serializer=StatusPaySerializer(statusPay,many=True)
            data=serializer.data
            return Response({'data':data,'success':True,'message':'Listado de los estados de pago'},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'data':data,'success':False,'message':'Error '+str(e)},status=status.HTTP_404_NOT_FOUND)