from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.


class Address(models.Model):
    street = models.CharField('Calle', max_length=255)
    number = models.IntegerField('Número')
    postalCode = models.IntegerField('Código postal')
    city = models.CharField('Ciudad', max_length=255)
    province = models.CharField('Provincia', max_length=255)
    reference = models.TextField('Referencia')


class User(models.Model):
    name = models.CharField('Nombre', max_length=255)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.DO_NOTHING, verbose_name='Dirección')
    email = models.CharField(max_length=255)


class ShopCart(models.Model):
    subtotal = models.FloatField('Sub total')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuario')
