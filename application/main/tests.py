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
        result_1, cat_1 = Product.retrieve_product(request_1)
        print(result_1)
        result_2, cat_2 = Product.retrieve_product(request_2)
        print(result_2)
        result_3, cat_3 = Product.retrieve_product(request_3)
        print(result_3)
        self.assertEqual(result_1.code, target_1)
        print('assert 1 DONE')
        self.assertEqual(result_2.code, target_2)
        print('assert 2 DONE')
        self.assertEqual(result_3.code, target_3)
        print('assert 3 DONE')
