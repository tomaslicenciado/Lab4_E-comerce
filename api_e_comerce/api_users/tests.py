from django.test import TestCase, Client
import json

from django.urls import reverse

from .models import User
from shop_cart.models import ShopCart, ShopCartDetail
from products.models import Product


# Create your tests here.
class UserTest(TestCase):
    def setUp(self):
        self.browser = Client()
        self.client = User.objects.create(username="pepe",
                                          email='pepe@pepe.com',
                                          password="pepe123",
                                          is_staff=True,
                                          is_active=True)
        self.client.set_password('pepe123')
        self.client.save()
        response = self.browser.post('/api/auth/login/', {'email': 'pepe@pepe.com', 'password': 'pepe123'})
        rj = json.loads(response.content)
        self.browser.defaults['HTTP_AUTHORIZATION'] = 'Bearer {}'.format(rj.get('access'))

    def test_api_add_user(self):
        user = dict(username='tom',
                    password='tom12345',
                    email='tom@admin.api',
                    first_name='Tomás',
                    last_name='Ferreyra')
        response = self.browser.post(reverse('register-list'), user)
        self.assertEqual(response.status_code, 201)
        self.shop_cart = ShopCart.objects.get(user=User.objects.last())
        self.assertEqual(self.shop_cart.subtotal, 0)
        self.prod1 = Product.objects.create(name='Mirinda',
                                            unit_price=150,
                                            unit_per_package=6,
                                            package_price=130 * 6,
                                            stock_unit=10)
        response = self.browser.post('/api/auth/login/', {'email': 'tom@admin.api', 'password': 'tom12345'})
        rj = json.loads(response.content)
        self.browser.defaults['HTTP_AUTHORIZATION'] = 'Bearer {}'.format(rj.get('access'))
        cart_detail = dict(product=1,
                           quantity=2)
        rsp = self.browser.post(reverse('prodCart-list'), json.dumps(cart_detail), content_type="application/json")
        self.assertEqual(rsp.status_code, 201)
        self.shop_cart = ShopCart.objects.get(user=User.objects.last())
        self.assertEqual(self.shop_cart.subtotal, 300)

    def test_change_attr_user(self):
        new_data = dict(username='Pepo',
                        first_name=self.client.first_name,
                        last_name=self.client.last_name)
        response = self.browser.patch(reverse('changeattr'), json.dumps(new_data), content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_change_pass_user(self):
        new_data = dict(password='pepe1234')
        response = self.browser.patch(reverse('changepassword'), json.dumps(new_data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        rsp = self.browser.post('/api/auth/login/', {'email': 'pepe@pepe.com', 'password': 'pepe1234'})
        self.assertEqual(rsp.status_code, 200)
