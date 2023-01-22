
from rest_framework  import serializers
from CobrosApp.models import Course


class CouserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'