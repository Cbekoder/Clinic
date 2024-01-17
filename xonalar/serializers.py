from rest_framework import serializers
from .models import Xona, Joylashtirish

class XonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Xona
        fields = '__all__'

class JoylashtirishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Joylashtirish
        fields = '__all__'