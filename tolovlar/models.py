from django.db import models

from register.models import *
from xonalar.models import *


class Tolov(models.Model):
    bemor = models.ForeignKey(Bemor, on_delete=models.CASCADE)
    joylashtirish = models.ForeignKey(Joylashtirish, on_delete=models.SET_NULL, null=True)
    yollanma = models.ForeignKey(Yollanma, on_delete=models.SET_NULL, null=True)
    summa = models.PositiveIntegerField()
    tolangan_summa = models.PositiveIntegerField(default=0)
    turi = models.CharField(max_length=50)
    izoh = models.CharField(max_length=100)
    tolandi = models.BooleanField(default=False)
    sana = models.DateField(auto_now_add=True)
    tolangan_sana = models.DateField(blank=True, null=True)

class QoshimchaTolov(models.Model):
    tolov = models.ForeignKey(Tolov, on_delete=models.CASCADE)
    sana = models.DateField(auto_now_add=True)
    summa = models.IntegerField()
    izoh = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return self.izoh