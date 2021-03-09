import requests, json
import pprint
from django.db import IntegrityError
from django.db.utils import DataError
from django.test import TestCase
from .models import Product


# Create your tests here.

class ProductModelTests(TestCase):
    """
    Class of tests functions for the Product model.
    """

    def setUp(self):
        with open('main/mock_tests_product.json', 'r') as mock_products:
            data = json.load(mock_products)
        test_products = data['products']
        for product in test_products:
            product = Product.objects.create(name=product['product_name'],
                                             code=product['code'],
                                             nutriscore=product['nutriscore_grade'],
                                             url=product['url'],
                                             popularity=product['unique_scans_n'])

    def test_retrieve_product(self):
        """
        retrive_product() returns the product matching with the search of the user.
        """
        target_1 = '5449000169327'  # Coca Cola zéro sans caféine
        target_2 = '3449860415703'  # Petits Bâtons de Berger Nature
        target_3 = '3175680011534'  # Biscuit lait chocolat
        request_1 = 'cola zéro coca caféine'
        request_2 = 'berger baton petit nature'
        request_3 = 'lait chocolat biscuit'
        self.assertEqual(Product.retrieve_product(self, request_1).code, target_1)
        print('assert 1 DONE')
        self.assertEqual(Product.retrieve_product(self, request_2).code, target_2)
        print('assert 2 DONE')
        self.assertEqual(Product.retrieve_product(self, request_3).code, target_3)
        print('assert 3 DONE')
