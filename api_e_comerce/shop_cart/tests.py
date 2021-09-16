from django.test import TestCase, Client
import json

from django.urls import reverse

from products.models import Product
from api_users.models import User
from sales.models import Sale, SaleDetail
from .models import ShopCart, ShopCartDetail


# Create your tests here.
class ProductTest(TestCase):
    def setUp(self):
        self.browser = Client()
        self.client = User.objects.create(username="pepe",
                                          email='pepe@pepe.com',
                                          password="pepe123",
                                          is_active=True)
        self.client.set_password('pepe123')
        self.client.save()
        self.shop_cart = ShopCart.objects.create(user=self.client)
        self.sale = Sale.objects.create(client=self.client)

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
        self.browser.defaults['HTTP_AUTHORIZATION'] ='Bearer {}'.format(rj.get('access'))

    def test_shop_cart(self):
        self.assertEqual(self.shop_cart.subtotal, 0)
        added_prod = dict(product=self.prod1.id,
                          quantity=2)
        response = self.browser.post(reverse('prodCart-list'), json.dumps(added_prod), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.shop_cart = ShopCart.objects.get(user=self.client)
        self.assertEqual(self.shop_cart.subtotal, 300)
        resp = self.browser.delete(reverse('prodCart-detail', kwargs={'pk': ShopCartDetail.objects.last().id}))
        self.assertEqual(resp.status_code, 204)
        self.shop_cart = ShopCart.objects.get(user=self.client)
        self.assertEqual(self.shop_cart.subtotal, 0)
        added_prod = dict(product=self.prod1.id,
                          quantity=2)
        response = self.browser.post(reverse('prodCart-list'), json.dumps(added_prod), content_type="application/json")
        added_prod = dict(product=self.prod2.id,
                          quantity=2)
        response = self.browser.post(reverse('prodCart-list'), json.dumps(added_prod), content_type="application/json")
        self.shop_cart = ShopCart.objects.get(user=self.client)
        self.assertEqual(self.shop_cart.subtotal, 640)
        resp = self.browser.delete(reverse('prodCart-detail', kwargs={'pk': ShopCartDetail.objects.last().id}))
        self.shop_cart = ShopCart.objects.get(user=self.client)
        self.assertEqual(self.shop_cart.subtotal, 300)
