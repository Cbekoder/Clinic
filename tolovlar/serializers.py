from rest_framework.serializers import ModelSerializer
from tolovlar.models import Tolov, QoshimchaTolov


class TolovSerializer(ModelSerializer):
    class Meta:
        model = Tolov
        fields = '__all__'

class QoshimchaTolovSerializer(ModelSerializer):
    class Meta:
        model = QoshimchaTolov
        fields = '__all__'