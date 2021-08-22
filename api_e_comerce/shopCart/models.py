from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product
# Create your models here.


class ShopState(models.Model):
    name = models.CharField('Nombre', max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Estado de carro'
        verbose_name_plural = 'Estados de carro'


class Address(models.Model):
    street = models.CharField('Calle', max_length=255)
    number = models.IntegerField('Número')
    postalCode = models.IntegerField('Código postal')
    city = models.CharField('Ciudad', max_length=255)
    province = models.CharField('Provincia', max_length=255)
    reference = models.TextField('Referencia')

    def __str__(self):
        return '{}, nº {} - {}'.format(self.street, self.number, self.province)

    class Meta:
        verbose_name = 'Dirección'
        verbose_name_plural = 'Direcciones'


class User(models.Model):
    name = models.CharField('Nombre', max_length=255)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.DO_NOTHING, verbose_name='Dirección')
    email = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'


class ShopCart(models.Model):
    subtotal = models.FloatField('Sub total')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuario')
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
    shopcart = models.ForeignKey(ShopCart, on_delete=models.CASCADE, verbose_name='Carro de compras')
    state = models.ForeignKey(ShopDetailState, on_delete=models.DO_NOTHING, verbose_name='Estado')

    def __str__(self):
        return 'Detalle nº {} de {}'.format(self.pk, self.shopcart)

    class Meta:
        verbose_name = 'Detalle de Carro de compras'
        verbose_name_plural = 'Detalle de Carro de compras'
