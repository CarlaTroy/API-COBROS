
from rest_framework  import serializers
from CobrosApp.models import CounterPassword

class CountPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = CounterPassword
        fields ='__all__'
