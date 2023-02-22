from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
class UserSerializer(serializers.ModelSerializer):

    #mapear la data
    password2=serializers.CharField(style={'input_type': 'password'},write_only=True)
    
    class Meta:
        model=User
        fields=['id','username','email','password','password2','is_staff']
        extra_kwargs={'password': {'write_only':True}}
    def save(self):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        ##validar password
        if password != password2:
            raise serializers.ValidationError(' El password de confirmación no coinciden')
        account = User(email=self.validated_data['email'],username=self.validated_data['username'])
        account.set_password(password)
        account.is_staff=self.validated_data['is_staff']
        account.save()
        return account 
    def update(self, instance, validated_data):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        ##validar password
        if password != password2:
            raise serializers.ValidationError(' El password de confirmación no coinciden')
        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)
        instance.set_password(password)
        instance.is_staff = validated_data.get("is_staff", instance.is_staff)
        instance.save()
        return instance
