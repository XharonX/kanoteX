from django.db import models
# Create your models here.


class SaleChannel(models.Model):

    shop = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    region = models.CharField(max_length=100, verbose_name='township',)

    def __str__(self):
        return f"{self.shop} - {self.location}"


class POS(models.Model):
    ...
