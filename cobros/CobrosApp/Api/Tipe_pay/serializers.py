
from rest_framework  import serializers
from CobrosApp.models import Tipe_Pay


class TypePaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipe_Pay
        fields = '__all__'