import json
from os import name
import pprint
from django.db import IntegrityError, transaction
from django.db.utils import DataError
from django.test import TestCase
from urllib.error import HTTPError, URLError
from .models import Product, Category
from django.core.management.base import CommandError
from django.core.management import call_command
from io import StringIO


# Create your tests here.

class ProductModelTests(TestCase):
    """
    Class of tests functions for the Product model.
    """

    def setUp(self):
        out = StringIO()
        call_command('db_create_categories', stdout=out)
        with open('main/mock_tests_product.json', 'r') as mock_products:
            data = json.load(mock_products)
        test_categories = data['categories']
        for key in test_categories:
            for sub in test_categories[key]:
                sub_category_name = sub
                main_category_name = key
                for product in data[sub_category_name]:
                    try:
                        with transaction.atomic():
                            main_category = Category.objects.get(name=main_category_name)
                            sub_category = Category.objects.get(name=sub_category_name)
                            product = Product(name=product['product_name'],
                                              code=product['code'],
                                              nutriscore=product['nutriscore_grade'],
                                              url=product['url'],
                                              popularity=product['unique_scans_n'])
                            product.save()
                            product.category.add(main_category)
                            product.category.add(sub_category)
                    except HTTPError:
                        pass
                    except URLError:
                        pass
                    except KeyError:
                        pass
                    except DataError:
                        pass
                    except IntegrityError:
                        pass

    def test_retrieve_product(self):
        """
        retrieve_product() returns the product matching with the search of the user.
        """
        print("\nTEST - Product --> def retrieve_product()\n")
        target_1 = '5449000169327'  # Coca Cola zéro sans caféine
        target_2 = '3449860415703'  # Petits Bâtons de Berger Nature
        target_3 = '3176582033334'  # camembert au lait pasteurisé
        request_1 = 'zéro coca-cola caféine'
        request_2 = 'berger bâtons petits nature'
        request_3 = 'lait camembert pasteurisé'
        result_1, cat_1 = Product.retrieve_product(request_1)
        result_2, cat_2 = Product.retrieve_product(request_2)
        result_3, cat_3 = Product.retrieve_product(request_3)
        print("self.assertEqual(result_1.code, '5449000169327')")
        self.assertEqual(result_1.code, target_1)
        print('assert 1 DONE')
        print("self.assertEqual(result_2.code, '3449860415703')")
        self.assertEqual(result_2.code, target_2)
        print('assert 2 DONE')
        print("self.assertEqual(result_3.code, '3176582033334')")
        self.assertEqual(result_3.code, target_3)
        print('assert 3 DONE')

    def test_looking_for_suggestion(self):
        """
        looking_for_suggestion() returns the suggestions from the category of the selected product.
        """
        print("\nTEST - Product --> def looking_for_suggestion()\n")
        target_1_code = '5449000169327'  # Coca Cola zéro sans caféine
        target_1 = Product.objects.get(code=target_1_code)
        target_1_category = Category.objects.filter(product__id=target_1.id)
        target_nutriscore, j = 'b', 1
        nb = Product.looking_for_suggestion(target_1_code, target_nutriscore, target_1_category, j)
        self.assertEqual(nb[0].name, 'Coca Zéro')
        print("assert DONE")

    def test_generate_suggestions(self):
        """
        When the user look for a product, he can chose an alternative one if there is.
        generate_suggestions() returns a list of maximum 6 alternative products of the same main or/and sub category.
        All the products returned have the same or a better nutriscore.
        """
        print("\nTEST - Product --> def generate_suggestions()\n")
        request_1 = 'zéro coca-cola caféine'
        request_2 = 'berger bâtons petits nature'
        request_3 = 'lait camembert pasteurisé'
        result_1, cat_1 = Product.retrieve_product(request_1)
        result_2, cat_2 = Product.retrieve_product(request_2)
        result_3, cat_3 = Product.retrieve_product(request_3)
        suggestions_1 = Product.generate_suggestions(cat_1, result_1)
        suggestions_2 = Product.generate_suggestions(cat_2, result_2)
        suggestions_3 = Product.generate_suggestions(cat_3, result_3)
        print("self.assertEqual(suggestions for 'zéro coca-cola caféine', 0")
        self.assertEqual(suggestions_1, 0)
        print("ASSERT 1 DONE")
        print("self.assertEqual(name of first suggestion for 'berger bâtons petits nature', 'Fine saveur de viande séchée'")
        self.assertEqual(suggestions_2[0].name, 'Fine saveur de viande séchée')
        print("ASSERT 2 DONE")
        print("self.assertEqual(name of first suggestion for 'lait camembert pasteurisé', 'SKYR'")
        self.assertEqual(suggestions_3[0].name, 'SKYR')
        print("ASSERT 3 DONE")


class DatabaseCommandsTests(TestCase):
    """
    Test functions for the database custom commands.
    """
    def setUp(self):
        out = StringIO()
        call_command('db_create_categories', stdout=out)
        with open('main/mock_tests_product.json', 'r') as mock_products:
            data = json.load(mock_products)
        test_categories = data['categories']
        for key in test_categories:
            for sub in test_categories[key]:
                sub_category_name = sub
                main_category_name = key
                for product in data[sub_category_name]:
                    try:
                        with transaction.atomic():
                            main_category = Category.objects.get(name=main_category_name)
                            sub_category = Category.objects.get(name=sub_category_name)
                            product = Product(name=product['product_name'],
                                              code=product['code'],
                                              nutriscore=product['nutriscore_grade'],
                                              url=product['url'],
                                              popularity=product['unique_scans_n'])
                            product.save()
                            product.category.add(main_category)
                            product.category.add(sub_category)
                    except HTTPError:
                        pass
                    except URLError:
                        pass
                    except KeyError:
                        pass
                    except DataError:
                        pass
                    except IntegrityError:
                        pass

    def test_categories(self):
        """
        Function checking the creation of the categories in the test database
        """
        print("\nTEST - Database Commands --> Categories\n")
        target_1 = 'camembert'
        target_2 = 'glace vanille'
        target_3 = 'jus de raisin'
        camembert = Category.objects.get(name=target_1)
        print("self.assertIn(str(camembert.id), '6')")
        self.assertIn(str(camembert.id), '6')
        print('Camembert DONE')
        vanilla = Category.objects.get(name=target_2)
        print("self.assertIn(str(vanilla.id), '17')")
        self.assertIn(str(vanilla.id), '17')
        print('vanilla DONE')
        grape = Category.objects.get(name=target_3)
        print("self.assertIn(str(grape.id), '37')")
        self.assertIn(str(grape.id), '37')
        print('grape DONE')

    def test_db_delete_category(self):
        """
        Function testing the custom command used to delete a precise category, main or sub.
        It also tests if the products of the deleted categories are deleted.
        """
        print("\nTEST - Database Commands --> def db_delete_category()\n")
        delete_1 = 'fromage bleu'
        delete_2 = 'yaourt'
        out = StringIO()
        call_command('db_delete_category', delete_1, stdout=out)
        categories = Category.objects.all()
        remaining = [category.name for category in categories]
        assert_1 = ["fromage", "fromage de vache", "fromage de chevre", "fromage tome", "camembert", "roquefort",
                    "livarot", "pont l'eveque", "yaourt", "yaourt nature", "yaourt aux fruits", "yaourt végétal",
                    "yaourt chocolat", "glace", "glace chocolat", "glace vanille", "glace sorbet fruit", "biscuit",
                    "biscuit chocolat", "biscuit beurre", "biscuit fruits", "soda", "soda cola", "limonade",
                    "soda fruits", "charcuterie", "jambon blanc", "saucisson sec", "chorizo", "jambon serrano",
                    "jambon parme", "jus de fruits", "jus d'orange", "jus de pomme", "jus multifruits", "jus de raisin"]
        print("self.assert(categories.name remaining, all but 'fromage bleu')")
        self.assertEqual(remaining, assert_1)
        print('Assert 1 Done')
        call_command('db_delete_category', delete_2, stdout=out)
        categories = Category.objects.all()
        remaining = [category.name for category in categories]
        assert_2 = ["fromage", "fromage de vache", "fromage de chevre", "fromage tome", "camembert", "roquefort",
                    "livarot", "pont l'eveque", "glace", "glace chocolat", "glace vanille", "glace sorbet fruit",
                    "biscuit", "biscuit chocolat", "biscuit beurre", "biscuit fruits", "soda", "soda cola", "limonade",
                    "soda fruits", "charcuterie", "jambon blanc", "saucisson sec", "chorizo", "jambon serrano",
                    "jambon parme", "jus de fruits", "jus d'orange", "jus de pomme", "jus multifruits", "jus de raisin"]
        print("self.assert(categories.name remaining, all but 'fromage bleu', 'yaourt' and its subs)")
        self.assertEqual(remaining, assert_2)
        print('Assert 2 Done')
