
import secrets
import string
from CobrosApp.Api.CountPassword.serializers import CountPasswordSerializer
from CobrosApp.models import CounterPassword
from django.core.mail import send_mail
from cobros.settings import EMAIL_HOST
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
                return {'data':[],'success':False,'message':'La contraseña es incorrecta, numero de intentos sobrantes '+str(intentos)}
            ##ya fallo mas de una vez
            cont=countPassword.count
            if cont<intentos:
                cont=cont + 1
                countPassword.count=cont
                countPassword.save()
                return {'data':[],'success':False,'message':'La contraseña es incorrecta, numero de intentos sobrantes '+str(intentos-cont)}
            ##enviar correo
            passwordRANDON=''
            pwd_length = 12
            letters = string.ascii_letters
            digits = string.digits
            special_chars = string.punctuation
            alphabet = letters + digits + special_chars
            for i in range(pwd_length):
                passwordRANDON += ''.join(secrets.choice(alphabet))
            user.set_password(passwordRANDON)
            user.save()
            countPassword.delete()
            email=send_mail(
                'Hola '+str(user.username)+' Nueva contraseña generado para su inicio de session ',
                'Su nueva contraseña generado para su inicio de session es '+'su contraseña es '+passwordRANDON,
                EMAIL_HOST,
                [user.email],
                fail_silently=False,
            )
            return {'data':email,'success':False,'message':'SE ENVIO UNA CONTRASEÑA NUEVA A SU CORREO  '+str(user.email)}           
        return None