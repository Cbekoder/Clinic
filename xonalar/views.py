from rest_framework.views import APIView
from .models import Xona, Joylashtirish
from register.models import Bemor
from tolovlar.models import Tolov
from rest_framework.response import Response
from .serializers import XonaSerializer, JoylashtirishSerializer
from rest_framework import status
from django.db import transaction
from datetime import datetime

class XonalarAPIView(APIView):
    def get(self, request):
        xonalar = Xona.objects.all()
        qarovchi = request.query_params.get('qarovchi')

        if qarovchi is not None:
            if qarovchi.lower() == 'true':
                xonalar = Xona.objects.filter(bosh_joy_soni__gte=1)
            elif qarovchi.lower() == 'false':
                xonalar = Xona.objects.filter(bosh_joy_soni__lt=2)
        serializer = XonaSerializer(xonalar, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class JoylashtirishlarAPIView(APIView):
    def get(self, request):
        joylashtirishlar = Joylashtirish.objects.order_by("-id")
        holat = request.query_params.get("holat")
        if holat == 'ketgan':
            joylashtirishlar = joylashtirishlar.filter(ketish_sana__isnull=False)
        elif holat == 'ketmagan':
            joylashtirishlar = joylashtirishlar.filter(ketish_sana__isnull=True)
        serializer = JoylashtirishSerializer(joylashtirishlar, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    # atomic transactions
    @transaction.atomic
    def post(self, request):
        joylashtirish = request.data
        serializer = JoylashtirishSerializer(data=joylashtirish)
        if serializer.is_valid():
            joylashtirish = serializer.save()

            bemor = Bemor.objects.get(id=joylashtirish.bemor.id)
            bemor.joylashgan = True
            bemor.save()

            xona = Xona.objects.get(id=joylashtirish.xona.id)
            if joylashtirish.qarovchi == True:
                xona.bosh_joy_soni -= 2
            else:
                xona.bosh_joy_soni -= 1
            xona.save()

            Tolov.objects.create(
                bemor=bemor,
                joylashtirish=joylashtirish,
                summa=0
            )

            return Response(serializer.data)
        return Response(serializer.errors)

class JoylashtirishUpdate(APIView):

    @transaction.atomic
    def put(self, request, pk):
        joylashtirish = Joylashtirish.objects.get(id=pk)
        serializer = JoylashtirishSerializer(joylashtirish, data=request.data)
        if serializer.is_valid():
            serializer.save()

            bemor = Bemor.objects.get(id=joylashtirish.bemor.id)
            bemor.joylashgan = False
            bemor.save()

            xona = Xona.objects.get(id=joylashtirish.xona.id)
            if joylashtirish.qarovchi == True:
                xona.bosh_joy_soni += 2
            else:
                xona.bosh_joy_soni += 1
            xona.save()

            tolov = Tolov.objects.get(joylashtirish=joylashtirish)
            d1 = datetime.strptime(datetime.today(), "%Y-%m-%d")
            d2 = datetime.strptime(joylashtirish.kelgan_sana, "%Y-%m-%d")
            joylashtirish.yotgan_kun_soni = abs(d1-d2)
            joylashtirish.save()
            summa = joylashtirish.yotgan_kun_soni * xona.narx
            if joylashtirish.qarovchi:
                summa *= 2
            tolov.summa = summa
            tolov.save()

            return Response(serializer.data)
        return Response(serializer.errors)