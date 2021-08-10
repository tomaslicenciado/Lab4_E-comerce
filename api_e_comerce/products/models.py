from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField('Nombre', max_length=255)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, default=None)


class Product(models.Model):
    name = models.CharField('Nombre', max_length=255)
    unit_price = models.FloatField('Precio Unitario')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, default=None)
    