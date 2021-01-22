from django.core.management import call_command
from django.test import TestCase, Client

from mainapp.models import ProductCategory, Product


class TestMainappSmoke(TestCase):

    def setUp(self):
        test_category = ProductCategory.objects.create(name='Test')
        Product.objects.create(
            category=test_category,
            name='Product test 1'
        )
        Product.objects.create(
            category=test_category,
            name='Product test 2'
        )
        self.client = Client

    def test_mainapp_urls(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/contacts')
        self.assertEqual(response.status_code, 200)



    def tearDown(self):
        call_command('sqlsequencereset', 'mainapp', 'authapp', 'ordersapp', 'basketapp')
