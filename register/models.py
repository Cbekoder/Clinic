from django.db import models

class Bemor(models.Model):
    ism = models.CharField(max_length=30)
    tel = models.CharField(max_length=13)
    manzil = models.CharField(max_length=100)
    joylashgan = models.BooleanField(default=False)

    def __str__(self):
        return self.ism


class Yollanma(models.Model):
    nom = models.CharField(max_length=50)
    narx = models.PositiveIntegerField()
    qayerga = models.CharField(
        max_length=30,
        choices=[
           ("UZI", "UZI"),
           ("Shifokor", "Shifokor"),
           ("Labaratoriya", "Laboratoriya")
        ]
    )

    def __str__(self):
        return self.nom
