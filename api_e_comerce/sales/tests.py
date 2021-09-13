from django.test import TestCase, Client
import json

from django.urls import reverse

from products.models import Product
from api_users.models import User
from .models import PayMethod, SaleDetail, Sale
from shop_cart.models import ShopCart


# Create your tests here.
class ProductTest(TestCase):
    def setUp(self):
        self.browser = Client()
        self.client = User.objects.create(username="pepe",
                                          email='pepe@pepe.com',
                                          password="pepe123",
                                          is_staff=True,
                                          is_active=True)
        self.client.set_password('pepe123')
        self.client.save()
        self.shop_cart = ShopCart.objects.create(user=self.client)
        self.pay_method = PayMethod.objects.create(name='Efectivo')
        self.prod1 = Product.objects.create(name='Mirinda',
                                            unit_price=150,
                                            unit_per_package=6,
                                            package_price=130 * 6,
                                            stock_unit=10)
        self.prod2 = Product.objects.create(name='Pritty',
                                            unit_price=170,
                                            unit_per_package=6,
                                            package_price=150 * 6,
                                            stock_unit=20)

        response = self.browser.post('/api/auth/login/', {'email': 'pepe@pepe.com', 'password': 'pepe123'})
        rj = json.loads(response.content)
        self.browser.defaults['HTTP_AUTHORIZATION'] = 'Bearer {}'.format(rj.get('access'))

    def test_direct_sale(self):
        chosen_prod = dict(pm=1,
                           delivery_cost=150,
                           product=1,
                           quantity=2)
        response = self.browser.post(reverse('directSale-list'), json.dumps(chosen_prod), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.prod1 = Product.objects.get(pk=self.prod1.pk)
        self.assertEqual(self.prod1.stock_unit, 8)
        self.sale = Sale.objects.last()
        self.assertEqual(self.sale.subtotal, 150 * 2)
