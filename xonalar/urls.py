from django.urls import path
from .views import JoylashtirishListAPIView, XonalarAPIView

urlpatterns = [
    path('xonalarni/', XonalarAPIView.as_view()),
    path('joylashtirishlar/', JoylashtirishListAPIView.as_view()),
]