from rest_framework import serializers
from django.contrib.auth.models import User

class RegistrationSerializer(serializers.ModelSerializer):

    #mapear la data
    password2=serializers.CharField(style={'input_type': 'password'},write_only=True)
    
    class Meta:
        model=User
        fields=['username','email','password','password2','is_staff']
        extra_kwargs={'password': {'write_only':True}}
    def save(self):
        password = self.validated_data['password']
        account = User(email=self.validated_data['email'],username=self.validated_data['username'])
        account.set_password(password)
        account.is_staff=self.validated_data['is_staff']
        account.save()
        return account 

############# ESTE ES EL Q FUNCIONA ##############
class UserSerializer(serializers.ModelSerializer):
    #mapear la data
    password2=serializers.CharField(style={'input_type': 'password'},write_only=True)
    class Meta:
        model = User
        fields = ('username', 'email', 'id', 'password','is_staff','password2')
        read_only_fields = ('id',)
        extra_kwargs = {
            'password': {'write_only': True}
        }
        """         def save(self):
                    password = self.validated_data['password']
                    account = User(email=self.validated_data['email'],username=self.validated_data['username'])
                    account.set_password(password)
                    account.is_staff=self.validated_data['is_staff']
                    account.save()
                    return account """
        """     def save(self,validated_data):
                account = User(email=self.validated_data['email'],username=self.validated_data['username'])
                password = self.validated_data['password']
                account.set_password(password)
                account.is_staff=self.validated_data['is_staff']
                account.save()
                return account """

    def update(self, instance, validated_data):
        #instance.username=validated_data.get('username',instance.username)
        """ instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)
        instance.about = validated_data.get("is_staff", instance.is_staff)
        instance.save()
        return instance """
        instance.username=validated_data.get('username',instance.username)
        instance.email=validated_data.get('email',instance.email)
        instance.password=validated_data.get('password',instance.password)
        instance.is_staff=validated_data.get('is_staff',instance.is_staff)
        instance.save() 
        return instance
"""     def delete(self, instance, validated_data):
        instance.delete()
        return instance  """