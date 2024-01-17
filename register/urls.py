from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BemorViewSet, YollanmaAPIView, BemorDetailAPIView

router = DefaultRouter()
router.register(r'bemor', BemorViewSet, basename='bemor')

urlpatterns = [
    path('', include(router.urls)),
    path('yollanmalar/', YollanmaAPIView.as_view()),
    path('bemor/<int:pk>/', BemorDetailAPIView.as_view()),
]