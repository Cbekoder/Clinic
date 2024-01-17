from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from xonalar.models import Joylashtirish
from register.models import Bemor
from .models import *
from .serializers import TolovSerializer

class TolovAPIView(APIView):
    def get(self, request):
        tolovlar = Tolov.objects.order_by("-id")
        serializer = TolovSerializer(tolovlar, many=True)
        return Response(serializer.data)