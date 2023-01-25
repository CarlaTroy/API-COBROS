
from rest_framework  import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username','email']
"""     def create(self, validated_data):
        data = {
                'name': validated_data.get('name', None),
                'date_init': validated_data.get('date_init', None),
                'date_end': validated_data.get('date_end', None),
                'cost_effective': validated_data.get('cost_effective', None),
                'cost_credit': validated_data.get('cost_credit', None),
                'course': validated_data.get('course_id', None)
                }
        return Cohorte.objects.create(**data) """
"""     def update(self,instancia,validated_data):
        instancia.name=validated_data.get('name',instancia.name)
        instancia.date_init=validated_data.get('date_init',instancia.date_init)
        instancia.date_end=validated_data.get('date_end',instancia.date_end)
        instancia.cost_effective=validated_data.get('cost_effective',instancia.cost_effective)
        instancia.cost_credit=validated_data.get('cost_credit',instancia.cost_credit)
        instancia.course=validated_data.get('course_id',instancia.course)
        instancia.save()
        return instancia  """