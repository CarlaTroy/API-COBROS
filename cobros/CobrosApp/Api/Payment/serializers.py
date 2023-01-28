
from rest_framework  import serializers
from CobrosApp.Api.Enrollement.serializers import EnrollementSerializer
from CobrosApp.Api.Status_Pay.serializers import StatusPaySerializer
from CobrosApp.models import Payment,Status_Pay,Enrollement

class PaymentSerializer(serializers.ModelSerializer):
    #user=UserSerializer(read_only=True)
    status_pay = StatusPaySerializer(read_only=True)
    status_pay_id=serializers.SlugRelatedField(queryset=Status_Pay.objects.all(),slug_field='id', write_only=True)
    
    enrollement = EnrollementSerializer(read_only=True)
    enrollement_id=serializers.SlugRelatedField(queryset=Enrollement.objects.all(),slug_field='id', write_only=True)


    class Meta:
        model = Payment
        fields = [  'id', 
                   'amount',
                   'date_pay',
                   'date_limit',
                   'status_pay', 
                   'status_pay_id',
                   'enrollement', 
                   'enrollement_id'
                ]
    def create(self, validated_data):
        data = {
            'amount': validated_data.get('amount', None),
            'date_pay': validated_data.get('date_pay', None),
            'date_limit': validated_data.get('date_limit', None),
            'status_pay': validated_data.get('status_pay_id', None),
            'enrollement': validated_data.get('enrollement_id', None)
            }
        return Payment.objects.create(**data)
"""     def update(self,instancia,validated_data):
        instancia.name=validated_data.get('name',instancia.name)
        instancia.last_name=validated_data.get('last_name',instancia.last_name)
        instancia.identification=validated_data.get('identification',instancia.identification)
        instancia.cell_phone=validated_data.get('cell_phone',instancia.cell_phone)
        instancia.address=validated_data.get('address',instancia.address)
        instancia.user=validated_data.get('user_id',instancia.user)
        instancia.save()
        return instancia """