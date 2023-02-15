
from CobrosApp.Api.CountPassword.serializers import CountPasswordSerializer
from CobrosApp.models import CounterPassword
from rest_framework.response import Response
from rest_framework import status
class CountPasswordValidate:
    def intent(user,password):        
        cont=0
        serializarCountPassword=None
        intentos=3
        if not user.check_password(password):
            countPassword=CounterPassword.objects.filter(username=user.username).first()
            ##primera vez que falla
            if not countPassword:
                dataCountPassword={
                    'username':user.username,
                    'count':cont
                }
                serializarCountPassword=CountPasswordSerializer(data=dataCountPassword)
                if serializarCountPassword.is_valid():
                    serializarCountPassword.save()
                return {'data':[],'success':False,'message':'La contraseña es incorrecta, numero de intentos sobrantes'+str(intentos-cont)}
            ##ya fallo mas de una vez
            cont=countPassword.count
            if cont<=intentos:
                cont=cont + 1
                countPassword.count=cont
                countPassword.save()
                return {'data':[],'success':False,'message':'La contraseña es incorrecta, numero de intentos sobrantes'+str(intentos-cont)}
            ##enviar correo
            countPassword.delete()
            return {'data':[],'success':False,'message':'SE ENVIO UN CORREO CON UNA NUEA CONTRASEÑ '+str(intentos-cont)+' intentos'}
        return None