from django.db import models
from api_users.models import User
from products.models import Product


class ShopState(models.Model):
    name = models.CharField('Nombre', max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Estado de carro'
        verbose_name_plural = 'Estados de carro'


class ShopCart(models.Model):
    subtotal = models.FloatField('Sub total')
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Usuario')
    state = models.ForeignKey(ShopState, on_delete=models.DO_NOTHING, verbose_name='Estado', default=None)

    def __str__(self):
        return 'Carro de compras de {}'.format(self.user)

    class Meta:
        verbose_name = 'Carro de compras'
        verbose_name_plural = 'Carros de compras'


class ShopDetailState(models.Model):
    name = models.CharField('Nombre', max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Estado de detalle de carro'
        verbose_name_plural = 'Estados de detalle de carro'


class ShopCartDetail(models.Model):
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, verbose_name='Producto')
    quantity = models.FloatField('Cantidad')
    subtotal = models.FloatField('Sub total')
    shopcart = models.ForeignKey(ShopCart, on_delete=models.CASCADE, verbose_name='Carro de compras', related_name='details')
    state = models.ForeignKey(ShopDetailState, on_delete=models.DO_NOTHING, verbose_name='Estado')

    def save(self, *args, **kwargs):
        if not self.id:
            cart = ShopCart.objects.get(pk=self.shopcart.id)
            cart.subtotal = cart.subtotal + self.subtotal
            cart.save()
        else:
            bd_state = ShopCartDetail.objects.get(pk=self.id).state
            if not self.state == bd_state:
                cart = ShopCart.objects.get(pk=self.shopcart.id)
                if self.state == ShopDetailState.objects.get(pk=1):
                    cart.subtotal = cart.subtotal + self.subtotal
                else:
                    cart.subtotal = cart.subtotal - self.subtotal
                cart.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return 'Detalle nº {} de {}'.format(self.pk, self.shopcart)

    class Meta:
        verbose_name = 'Detalle de Carro de compras'
        verbose_name_plural = 'Detalle de Carro de compras'
