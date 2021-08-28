import datetime
from django.db import models
from products.models import Product, Supplier
# Create your models here.


class Stock(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.DO_NOTHING, verbose_name='Proveedor')
    total = models.FloatField('Total', default=0)
    date = models.DateTimeField('Fecha', default=datetime.datetime.now)


class StockDetail(models.Model):
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, verbose_name='Producto')
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, verbose_name='Stock', related_name='details')
    quantity = models.FloatField('Cantidad')
    subtotal = models.FloatField('Sub total')

    def save(self, *args, **kwargs):
        stck = Stock.objects.get(pk=self.stock.id)
        stck.total = stck.total + self.subtotal
        stck.save()
        super().save( *args, **kwargs)


