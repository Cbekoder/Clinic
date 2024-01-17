from rest_framework.serializers import ModelSerializer
from .models import Tolov


class TolovSerializer(ModelSerializer):
    class Meta:
        model = Tolov
        fields = '__all__'