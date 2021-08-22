import datetime
from django.db import models
from products.models import Product, Supplier
# Create your models here.


class Stock(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.DO_NOTHING, verbose_name='Proveedor')
    total = models.FloatField('Total')
    date = models.DateTimeField('Fecha', default=datetime.datetime.now)


class StockDetail(models.Model):
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, verbose_name='Producto')
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, verbose_name='Stock')
    quantity = models.FloatField('Cantidad')
    subtotal = models.FloatField('Sub total')
