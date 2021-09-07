from django.db import models
from api_users.models import User
from products.models import Product


class ShopCart(models.Model):
    subtotal = models.FloatField('Sub total')
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Usuario')

    def __str__(self):
        return 'Carro de compras de {}'.format(self.user)

    class Meta:
        verbose_name = 'Carro de compras'
        verbose_name_plural = 'Carros de compras'


class ShopCartDetail(models.Model):
    OPEN = 1
    SELL = 2
    CANCELED = 3
    STATES = ((OPEN, "En carro"),
              (SELL, "Vendido"),
              (CANCELED, "Cancelado"),)

    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, verbose_name='Producto')
    quantity = models.FloatField('Cantidad')
    subtotal = models.FloatField('Sub total')
    shopcart = models.ForeignKey(ShopCart, on_delete=models.CASCADE, verbose_name='Carro de compras',
                                 related_name='details', default=0)
    state = models.SmallIntegerField("Estado", default=OPEN, choices=STATES)

    def save(self, *args, **kwargs):
        self.subtotal = self.product.unit_price * self.quantity
        if not self.id:
            self.shopcart.subtotal += self.subtotal
            self.shopcart.save()
        else:
            bd_state = ShopCartDetail.objects.get(pk=self.id).state
            if not self.state == bd_state:
                if self.state == self.OPEN:
                    self.shopcart.subtotal += self.subtotal
                else:
                    self.shopcart.subtotal -= self.subtotal
                self.shopcart.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return 'Detalle nº {} de {}'.format(self.pk, self.shopcart)

    class Meta:
        verbose_name = 'Detalle de Carro de compras'
        verbose_name_plural = 'Detalle de Carro de compras'
