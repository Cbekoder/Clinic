from rest_framework import viewsets
from .models import Bemor, Yollanma
from .serializers import BemorSerializer, YollanmaSerializer
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

class BemorViewSet(viewsets.ModelViewSet):
    serializer_class = BemorSerializer
    queryset = Bemor.objects.all().order_by('-id')
    filter_backends = [filters.SearchFilter]
    search_fields = ['ism', 'tel']

class BemorDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = Bemor.objects.all()
    serializer_class = BemorSerializer
    lookup_field = 'pk'

class YollanmaAPIView(APIView):
    def get(self, request):
        yollanmalar = Yollanma.objects.all().order_by('-id')
        serializer = YollanmaSerializer(yollanmalar, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = YollanmaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
