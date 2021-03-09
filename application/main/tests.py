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

    def test_retrieve_product(self):
        """
        retrive_product() returns the product matching with the search of the user.
        """
        target_1 = '5449000169327'  # Coca Cola zéro sans caféine
        target_2 = '3449860415703'  # Petits Bâtons de Berger Nature
        target_3 = '3175680011534'  # Biscuit lait chocolat
        request_1 = 'coca cola zéro sans caféine'
        request_2 = 'Petit bâton berger nature'
        request_3 = 'biscuit lait chocolat'
        self.assertEqual(Product.retrieve_product(self, request_1), target_1)
        self.assertEqual(Product.retrieve_product(self, request_2), target_2)
        self.assertEqual(Product.retrieve_product(self, request_3), target_3)
