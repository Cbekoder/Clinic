from rest_framework import serializers
from .models import Bemor, Yollanma

class BemorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bemor
        fields = '__all__'

class YollanmaSerializer(serializers.ModelSerializer):
    class Meta:
        models = Yollanma
        fields = '__all__'