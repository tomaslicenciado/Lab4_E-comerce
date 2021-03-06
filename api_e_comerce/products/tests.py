
from django.test import TestCase, Client
import json

from django.urls import reverse
from rest_framework import response

from .models import Product
from api_users.models import User
from sales.models import Sale, SaleDetail
from shop_cart.models import ShopCart, ShopCartDetail


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
        self.prod3 = Product.objects.create(name='Inactivo',
                                            unit_price=170,
                                            unit_per_package=6,
                                            package_price=150 * 6,
                                            stock_unit=20,
                                            active=False)

        self.cart_detail = ShopCartDetail.objects.create(product=self.prod1,
                                                         quantity=2,
                                                         shopcart=self.shop_cart)

        response = self.browser.post('/api/auth/login/', {'email': 'pepe@pepe.com', 'password': 'pepe123'})
        rj = json.loads(response.content)
        self.browser.defaults['HTTP_AUTHORIZATION'] ='Bearer {}'.format(rj.get('access'))

    def test_create_product(self):
        cnt = Product.objects.count()
        self.assertEqual(cnt, 3)
        mirinda = Product.objects.get(name='Mirinda')
        self.assertEqual(mirinda.stock_unit, 10)

    def test_detail_cart(self):
        self.assertEqual(self.shop_cart.subtotal, 150 * 2)
        self.assertEqual(self.cart_detail.subtotal, 150 * 2)

    def test_check_stock(self):
        sale_detail = SaleDetail.objects.create(sale=self.sale,
                                                shop_cart_detail=self.cart_detail)
        self.assertEqual(self.prod1.stock_unit, 8)
        self.assertEqual(self.sale.subtotal, 150 * 2)

    def test_api_products(self):
        doesnotexist = self.browser.get('/api/no-existe/')
        self.assertEqual(doesnotexist.status_code, 404)
        products = self.browser.get(reverse('products-list'))
        self.assertEqual(products.status_code, 200)
        content = json.loads(products.content)
        self.assertEqual(len(content), 3)
        self.assertIsNotNone(content[0].get("name"))
        self.assertIsNone(content[0].get("cualquierotracosa"))

    def test_api_add_product(self):
        saladix = dict(name='Saladix',
                       unit_price=80,
                       unit_per_package=24,
                       package_price=50 * 24,
                       stock_unit=5)
        response = self.browser.post(reverse('products-list'), saladix)
        self.assertEqual(response.status_code, 201)
        cnt = Product.objects.count()
        self.assertEqual(cnt, 4)
        last = Product.objects.last()
        response = self.browser.delete(reverse('products-detail', args=[last.pk]))
        cnt = Product.objects.count()
        self.assertEqual(cnt, 3)

    def test_api_stock(self):
        page = reverse('setAddStock-list')
        prod1 = [dict(id=1, stock_unit=15), ]
        prod2 = [dict(id=1, stock_unit=-1), ]
        prod3 = [dict(id=1, stock_unit=15), dict(id=2, stock_unit=25)]
        prod4 = [dict(id=1, stock_unit=15), dict(id=3, stock_unit=15)]
        prod5 = [dict(id=1, stock_unit=15), dict(id=20, stock_unit=15)]
        response = self.browser.post(page, json.dumps(prod1), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.prod1 = Product.objects.get(pk=self.prod1.pk)
        self.assertEqual(self.prod1.stock_unit, 15)
        response = self.browser.post(page, json.dumps(prod2), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        response = self.browser.post(page, json.dumps(prod3), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.prod2 = Product.objects.get(pk=self.prod2.pk)
        self.assertEqual(self.prod2.stock_unit, 25)
        response = self.browser.post(page, json.dumps(prod4), content_type="application/json")
        self.assertEqual(response.status_code, 406)
        response = self.browser.post(page, json.dumps(prod5), content_type="application/json")
        self.assertEqual(response.status_code, 404)
