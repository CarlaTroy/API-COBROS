
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
"""     def update(self,instancia,validated_data):
        instancia.name=validated_data.get('name',instancia.name)
        instancia.date_init=validated_data.get('date_init',instancia.date_init)
        instancia.date_end=validated_data.get('date_end',instancia.date_end)
        instancia.cost_effective=validated_data.get('cost_effective',instancia.cost_effective)
        instancia.cost_credit=validated_data.get('cost_credit',instancia.cost_credit)
        instancia.course=validated_data.get('course_id',instancia.course)
        instancia.save()
        return instancia """