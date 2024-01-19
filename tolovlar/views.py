from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Sum
from .models import Tolov
from .serializers import TolovSerializer, QoshimchaTolovSerializer
from django.db import transaction

class TolovAPIView(APIView):
    serializer_class = TolovSerializer
    pagination_class = PageNumberPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["sana", "tolangan_sana", "bemor__ism", "tolandi", "yollanma"]
    def get(self, request):
        tolovlar = Tolov.objects.all().order_by('-id')
        turi = request.query_params.get("turi")
        if turi == 'yollanma':
            tolovlar = tolovlar.filter(yollanma__isnull=False)
        elif turi == 'joylashtirish':
            tolovlar = tolovlar.filter(joylashtirish__isnull=False)

        sana = request.query_params.get('sana')
        bosh_sana = request.query_params.get('bosh_sana')
        yakun_sana = request.query_params.get('yakun_sana')
        if sana:
            tolovlar = Tolov.objects.filter(sana=sana) | Tolov.objects.filter(tolangan_sana=sana)
        if bosh_sana and yakun_sana:
            tolovlar = Tolov.objects.filter(sana__range=[bosh_sana, yakun_sana]) | Tolov.objects.filter(
                tolangan_sana__range=[bosh_sana, yakun_sana])
        serializer = TolovSerializer(tolovlar, many=True)
        tushum = tolovlar.aggregate(s=Sum("tolangan_summa")).get("s")
        if tushum is None:
            tushum = 0
        qarz = tolovlar.aggregate(s=Sum("summa")).get("s")
        if qarz is None:
            qarz = 0
        else:
            qarz -= tushum
        result = {
            "tolovlar": serializer.data,
            "umumiy_tushum": tushum,
            "qarzdorlik": qarz
        }
        return Response(result)

class TolovAPI(APIView):
    def put(self, request, pk):
        tolov = Tolov.objects.get(id=pk)
        serializer = TolovSerializer(tolov, data=request.data)
        if serializer.is_valid():
            serializer.save(
                    tolandi=serializer.data.get('tolangan_summa') == serializer.data.get("summa")
                )
            return Response(serializer.data)
        return Response(serializer.errors)

class QoshimchaTolov(APIView):
    def get(self, request):
        qtolovlar = QoshimchaTolov.objects.all()
        serializer = QoshimchaTolovSerializer(qtolovlar, many=True)
        return Response(serializer.data)

    @transaction.atomic()
    def post(self, request):
        qoshimchaTolov = request.data
        serializer = QoshimchaTolovSerializer(data=qoshimchaTolov)
        if serializer.is_valid():
            qoshimcha = serializer.save()

            tolov = Tolov.objects.get(id=qoshimcha.tolov)
            if tolov.summa == tolov.tolangan_summa + qoshimcha.summa:
                tolov.tolandi = True
                tolov.save()

            return Response(serializer.data)
        return Response(serializer.errors)