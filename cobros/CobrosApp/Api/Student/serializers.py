
from rest_framework  import serializers
from CobrosApp.models import Student
from django.contrib.auth.models import User
from CobrosApp.Api.User.serializers import UserSerializer

class StudentSerializer(serializers.ModelSerializer):
    #user=UserSerializer(read_only=True)
    user = UserSerializer(read_only=True)
    user_id=serializers.SlugRelatedField(queryset=User.objects.all(),slug_field='id', write_only=True)

    class Meta:
        model = Student
        fields = [  'id', 
                   'name',
                   'last_name',
                   'identification', 
                   'cell_phone',
                   'address', 
                   'user',
                   'user_id',
                ]
    def create(self, validated_data):
        data = {
            'name': validated_data.get('name', None),
            'last_name': validated_data.get('last_name', None),
            'identification': validated_data.get('identification', None),
            'cell_phone': validated_data.get('cell_phone', None),
            'address': validated_data.get('address', None),
            'user': validated_data.get('user_id', None)
            }
        return Student.objects.create(**data)
    def update(self,instancia,validated_data):
        instancia.name=validated_data.get('name',instancia.name)
        instancia.last_name=validated_data.get('last_name',instancia.last_name)
        instancia.identification=validated_data.get('identification',instancia.identification)
        instancia.cell_phone=validated_data.get('cell_phone',instancia.cell_phone)
        instancia.address=validated_data.get('address',instancia.address)
        instancia.user=validated_data.get('user_id',instancia.user)
        instancia.save()
        return instancia