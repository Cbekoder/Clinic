from django.db import models
from register.models import Bemor

class Xona(models.Model):
    qavat = models.PositiveSmallIntegerField()
    raqam = models.CharField(max_length=10)
    tur = models.CharField(
        max_length=15,
        choices=[
            ('Luks', 'Luks'),
            ('Yarim-luks', 'Yarim-luks'),
            ('Oddiy', 'Oddiy'),
        ]
    )
    sigim = models.PositiveSmallIntegerField()
    narx = models.PositiveIntegerField()
    bosh_joy_soni = models.PositiveSmallIntegerField()

    def __str__(self):
        return f'{self.qavat}, {self.raqam}-xona'

class Joylashtirish(models.Model):
    bemor = models.ForeignKey(Bemor, on_delete=models.SET_NULL, null=True)
    xona = models.ForeignKey(Xona, on_delete=models.SET_NULL, null=True)
    izoh = models.CharField(max_length=100, blank=True)
    kelgan_sana = models.DateField()
    ketish_sana = models.DateField()
    yotgan_kun_soni = models.PositiveSmallIntegerField(default=0)
    qarovchi = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.bemor.ism} {self.xona} da."