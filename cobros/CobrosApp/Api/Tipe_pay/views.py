from CobrosApp.Api.Tipe_pay.serializers import TypePaySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from CobrosApp.models import Tipe_Pay
class TypePayseAV(APIView):
    def get(self, request):
        data=None
        try:
            courses=Tipe_Pay.objects.all()
            serializer=TypePaySerializer(courses,many=True)
            data=serializer.data
            return Response({'data':data,'succes':True,'message':'Listado de los tipos de pagos'},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'data':data,'succes':False,'message':'Error '+str(e)},status=status.HTTP_404_NOT_FOUND)