from django.db import models
from shop_cart.models import ShopCartDetail
from products.models import Product
from api_users.models import User


class PayMethod(models.Model):
    name = models.CharField('Nombre', max_length=255)


class Sale(models.Model):
    pay_method = models.ForeignKey(PayMethod, on_delete=models.DO_NOTHING, default=None, verbose_name='Forma de pago')
    subtotal = models.FloatField('Sub total')
    delivery_cost = models.FloatField('Costo de envío')
    total = models.FloatField('Total')
    client = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Cliente')


class SaleDetail(models.Model):
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, verbose_name='Producto')
    quantity = models.FloatField('Cantidad')
    subtotal = models.FloatField('Sub total')
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, verbose_name='Venta', related_name='detail')
    shop_cart_detail = models.ForeignKey(ShopCartDetail, on_delete=models.DO_NOTHING, verbose_name='Detalle de carro')