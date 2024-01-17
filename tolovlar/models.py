from django.db import models
from register.models import Bemor, Yollanma
from xonalar.models import Joylashtirish

class Tolov(models.Model):
    bemor = models.ForeignKey(Bemor, on_delete=models.CASCADE)
    yollanma = models.ForeignKey(Yollanma, on_delete=models.SET_NULL, null=True)
    joylashtirish = models.ForeignKey(Joylashtirish, on_delete=models.SET_NULL, null=True)
    summa = models.PositiveIntegerField()
    tolangan_summa = models.PositiveIntegerField(default=0)
    tolandi = models.BooleanField(default=False)
    sana = models.DateField(auto_now_add=True)
    tolangan_sana = models.DateField(null=True, blank=True)
    turi = models.CharField(max_length=50)
    izoh = models.CharField(max_length=100, blank=True)


