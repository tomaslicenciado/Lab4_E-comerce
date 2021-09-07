from django.db import models
from shop_cart.models import ShopCartDetail
from products.models import Product
from api_users.models import User


class PayMethod(models.Model):
    name = models.CharField('Nombre', max_length=255)


class Sale(models.Model):
    pay_method = models.ForeignKey(PayMethod, on_delete=models.DO_NOTHING, default=None, null=True,
                                   verbose_name='Forma de pago')
    subtotal = models.FloatField('Sub total', default=0)
    delivery_cost = models.FloatField('Costo de envío', default=0)
    total = models.FloatField('Total', default=0)
    client = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Cliente')

    def save(self, *args, **kwargs):
        self.total = self.subtotal + self.delivery_cost
        super().save(*args, **kwargs)


class SaleDetail(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, verbose_name='Venta', related_name='detail')
    shop_cart_detail = models.ForeignKey(ShopCartDetail, on_delete=models.DO_NOTHING, verbose_name='Detalle de carro')

    def save(self, *args, **kwargs):
        self.shop_cart_detail.product.stock_unit -= self.quantity
        self.shop_cart_detail.product.save()
        self.sale.subtotal += self.subtotal
        self.sale.save()
        self.shop_cart_detail.state = ShopDetailState.SELL
        self.shop_cart_detail.save()
        super().save(*args, **kwargs)
