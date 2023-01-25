
from rest_framework  import serializers
from CobrosApp.Api.Cohorte.serializers import CohorteSerializer
from CobrosApp.Api.Student.serializers import StudentSerializer
from CobrosApp.models import Student,Tipe_Pay,Cohorte,Enrollement
from CobrosApp.Api.Tipe_pay.serializers import TypePaySerializer

class EnrollementSerializer(serializers.ModelSerializer):
    #user=UserSerializer(read_only=True)
    student = StudentSerializer(read_only=True)
    student_id=serializers.SlugRelatedField(queryset=Student.objects.all(),slug_field='id', write_only=True)
    
    cohorte = CohorteSerializer(read_only=True)
    cohorte_id=serializers.SlugRelatedField(queryset=Cohorte.objects.all(),slug_field='id', write_only=True)
    
    tipe_pay = TypePaySerializer(read_only=True)
    tipe_pay_id=serializers.SlugRelatedField(queryset=Tipe_Pay.objects.all(),slug_field='id', write_only=True)

    class Meta:
        model = Enrollement
        fields = [  'id', 
                   'student',
                   'student_id',
                   'cohorte', 
                   'cohorte_id',
                   'tipe_pay', 
                   'tipe_pay_id',
                   'cuotas',
                   'day_limite',
                    'cash',
                    'discount',
                ]
    def create(self, validated_data):
        data = {
            'student': validated_data.get('student_id', None),
            'cohorte': validated_data.get('cohorte_id', None),
            'tipe_pay': validated_data.get('tipe_pay_id', None),
            'cuotas': validated_data.get('cuotas', None),
            'day_limite': validated_data.get('day_limite', None),
            'cash': validated_data.get('cash', None),
            'discount': validated_data.get('discount', None)
            }
        return Enrollement.objects.create(**data)
"""     def update(self,instancia,validated_data):
        instancia.name=validated_data.get('name',instancia.name)
        instancia.last_name=validated_data.get('last_name',instancia.last_name)
        instancia.identification=validated_data.get('identification',instancia.identification)
        instancia.cell_phone=validated_data.get('cell_phone',instancia.cell_phone)
        instancia.address=validated_data.get('address',instancia.address)
        instancia.user=validated_data.get('user_id',instancia.user)
        instancia.save()
        return instancia """