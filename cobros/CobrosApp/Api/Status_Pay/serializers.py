
from rest_framework  import serializers
from CobrosApp.models import Tipe_Pay


class StatusPaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipe_Pay
        fields = '__all__'