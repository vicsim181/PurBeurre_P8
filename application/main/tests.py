# import json
# from django.db import IntegrityError, transaction
# from django.db.utils import DataError
from django.test import TestCase, RequestFactory
# from urllib.error import HTTPError, URLError
from .models import Product, Category, Store
from .views import HomeView, ResultsView, ProductView, MentionsView, CategoriesView
from django.core.management import call_command
from io import StringIO
from authentication.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver


# Create your tests here.
class ProductModelTests(TestCase):
    """
    Class of tests functions for the Product model.
    """
    fixtures = ['users.json']

    def test_retrieve_product(self):
        """
        retrieve_product() returns the product matching with the search of the user.
        """
        print("\nTEST - Product --> def retrieve_product()\n")
        target_1 = '5449000169327'  # Coca Cola zéro sans caféine
        target_2 = '3449860415703'  # Petits Bâtons de Berger Nature
        target_3 = '7622210450029'  # Prince - Biscuits fourrés goût lait choco
        target_4 = '5449000267443'  # coca-cola vanille
        request_1 = 'zéro sans coca-cola caféine'
        request_2 = 'berger bâtons petits nature'
        request_3 = 'prince biscuit'
        request_4 = 'coca vanille cola'
        result_1, cat_1 = Product.retrieve_product(request_1)
        result_2, cat_2 = Product.retrieve_product(request_2)
        result_3, cat_3 = Product.retrieve_product(request_3)
        result_4, cat_4 = Product.retrieve_product(request_4)
        print("self.assertEqual(result_1.code, '5449000169327')")
        self.assertEqual(result_1.code, target_1)
        print('assert 1 DONE')
        print("self.assertEqual(result_2.code, '3449860415703')")
        self.assertEqual(result_2.code, target_2)
        print('assert 2 DONE')
        print("self.assertEqual(result_3.code, '7622210450029')")
        self.assertEqual(result_3.code, target_3)
        print('assert 3 DONE')
        print("self.assertEqual(result_4.code, '5449000267443')")
        self.assertEqual(result_4.code, target_4)
        print('assert 4 DONE')
        product_test = Product.objects.get(code=target_3)
        print("self.assertEqual(print(product_test), 'product: prince - biscuits fourrés goût lait choco')")
        self.assertEqual(product_test.__str__(), 'product: prince - biscuits fourrés goût lait choco')
        print('assert 5 DONE')

    def test_retrieve_product_with_pk(self):
        """
        retrieve_prod_with_pk() returns the product matching with the pk, if it exists.
        """
        print("\nTEST - Product --> def retrieve_prod_with_pk()\n")
        print("camembert = Product.objects.get(code='3176582033334')")
        camembert = Product.objects.get(code='3176582033334')
        print("test_product = Product.retrieve_prod_with_pk(camembert.id)")
        test_product = Product.retrieve_prod_with_pk(camembert.id)
        print("self.assertEqual(test_product.__str__(), 'product: Camembert au lait pasteurisé')")
        self.assertEqual(test_product.__str__(), 'product: camembert au lait pasteurisé')
        print("ASSERT DONE")

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
        self.assertEqual(nb[0].name, 'coca zéro')
        print("assert DONE")

    def test_generate_suggestions(self):
        """
        When the user look for a product, he can chose an alternative one if there is.
        generate_suggestions() returns a list of maximum 6 alternative products of the same main or/and sub category.
        All the products returned have the same or a better nutriscore.
        """
        print("\nTEST - Product --> def generate_suggestions()\n")
        request_1 = 'zéro coca-cola caféine'
        request_2 = 'Spécialité saucisson sec'
        request_3 = 'lait camembert pasteurisé'
        result_1, cat_1 = Product.retrieve_product(request_1)
        result_2, cat_2 = Product.retrieve_product(request_2)
        result_3, cat_3 = Product.retrieve_product(request_3)
        suggestions_1 = Product.generate_suggestions(cat_1, result_1)
        suggestions_2 = Product.generate_suggestions(cat_2, result_2)
        suggestions_3 = Product.generate_suggestions(cat_3, result_3)
        print("self.assertEqual(suggestions for 'zéro coca-cola caféine', 0)")
        self.assertEqual(suggestions_1, 0)
        print("ASSERT 1 DONE")
        print("self.assertEqual(name of first suggestion for 'Spécialité saucisson sec', 'Le Bon Paris')")
        self.assertEqual(suggestions_2[1].name, 'le bon paris')
        print("ASSERT 2 DONE")
        print("self.assertEqual(name of first suggestion for 'lait camembert pasteurisé', 'chips camembert bret’s'")
        self.assertEqual(suggestions_3[0].name, "chips camembert bret’s")
        print("ASSERT 3 DONE")


class DatabaseCommandsTests(TestCase):
    """
    Test functions for the database custom commands.
    Also holds a test for the __str__() function of the Category Model.
    """
    fixtures = ['users.json']

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
        print("self.assertEqual(print(grape), 'category: jus de raisin')")
        self.assertEqual(grape.__str__(), 'category: jus de raisin')
        print('ASSERT DONE')

    def test_db_delete_category(self):
        """
        Function testing the custom command used to delete a precise category, main or sub.
        It also tests if the products of the deleted categories are deleted.
        """
        print("\nTEST - Database Commands --> def db_delete_category()\n")
        delete_1 = 'fromage bleu'
        delete_2 = 'yaourt'
        product_target = 'soja greek style'
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
        result_product, not_used = Product.retrieve_product(product_target)
        print("self.assertEqual(result from retrieve_product('soja greek style'), None)")
        self.assertEqual(result_product, None)
        print('Assert 3 Done')


class StoreModelTests(TestCase):
    """
    Test class for the Store Model.
    """
    def setUp(self):
        store = Store(name='Auchan')
        store.save()

    def test_str_(self):
        print("\nTEST - Store --> def __str__()\n")
        store = Store.objects.get(name="Auchan")
        print("self.assertEqual(print(store), 'store: Auchan')")
        self.assertEqual(store.__str__(), "store: Auchan")
        print("ASSERT DONE")


class HomeViewTests(TestCase):
    """
    Test class for HomeView.
    """
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='test', email='essaitest@gmail.fr', password='essaimdp+88')

    def test_homeview_get(self):
        print("\nTEST - HOMEVIEW --> def get()\n")
        request = self.factory.get('')
        request.user = self.user
        response = HomeView.as_view()(request)
        print("self.assertEqual(response.status_code, 200)")
        self.assertEqual(response.status_code, 200)
        print('Assert Done')


class ResultsViewTests(TestCase):
    """
    Test class for ResultsView.
    """
    fixtures = ['users.json']

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='test', email='essaitest@gmail.fr', password='essaimdp+88')

    def test_resultview_get(self):
        print("\nTEST - RESULTVIEW --> def get()\n")
        request_1 = self.factory.get('results/', data={'recherche': 'saucisson sec'})
        request_1.user = self.user
        response_1 = ResultsView.as_view()(request_1)
        request_2 = self.factory.get('results/', data={'recherche': 'gateau chocolat'})
        request_2.user = self.user
        response_2 = ResultsView.as_view()(request_2)
        print("self.assertEqual(ResultsView.as_view()(request, user_input='saucisson sec').status_code, 200)")
        self.assertEqual(response_1.status_code, 200)
        print('Assert Done')
        print("self.assertEqual(ResultsView.as_view()(request, user_input='gateau chocolat').status_code, 200)")
        self.assertEqual(response_2.status_code, 200)
        print('Assert Done')


class ProductViewTests(TestCase):
    """
    Test class for ProductView.
    """
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='test',
                                             email='essaitest@gmail.fr',
                                             password='essaimdp+88')
        self.test_product = Product(code="5449000000996",
                                    url="https://fr.openfoodfacts.org/produit/5449000000996/coca-cola",
                                    nutriscore="e",
                                    name="Coca-Cola Classic",
                                    popularity=2802)
        self.test_product.save()

    def test_productview_get(self):
        print("\nTEST - PRODUCTVIEW --> def get()\n")
        request = self.factory.get('product/', )
        request.user = self.user
        test_product = Product.objects.get(code='5449000000996')
        response = ProductView.as_view()(request, pk=test_product.id)
        print("self.assertEqual(response.status_code, 200)")
        self.assertEqual(response.status_code, 200)
        print('Assert Done')


class TestMentionsView(TestCase):
    """
    Test class for the MentionsView.
    """
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='test',
                                             email='essaitest@gmail.fr',
                                             password='essaimdp+88')

    def test_mentionsview_get(self):
        print("\nTEST - MENTIONSVIEW --> def get()\n")
        request = self.factory.get('mentionslegales/', )
        request.user = self.user
        response = MentionsView.as_view()(request)
        print("self.assertEqual(response.status_code, 200)")
        self.assertEqual(response.status_code, 200)
        print('Assert Done')


class TestCategoriesView(TestCase):
    """
    Test class for CategoriesView.
    """
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='test',
                                             email='essaitest@gmail.fr',
                                             password='essaimdp+88')

    def test_categoriesview_get(self):
        print("\nTEST - CATEGORIESVIEW --> def get()\n")
        request = self.factory.get('categories/', )
        request.user = self.user
        response = CategoriesView.as_view()(request)
        print("self.assertEqual(response.status_code, 200)")
        self.assertEqual(response.status_code, 200)
        print('Assert Done')


class UserStoriesMainTest(StaticLiveServerTestCase):
    """
    Main User stories: 2 user stories about searching a product.
    Selenium is used to realise the following tests.
    """
    fixtures = ['users.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser = WebDriver()
        cls.browser.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def test_looking_for_existing_product(self):
        """
        User look for the product 'camembert au lait cru' and see if a product exists matching the request.
        """
        self.browser.get(self.live_server_url)
        self.browser.maximize_window()
        self.browser.find_element_by_id('log in').click()
        username_input = self.browser.find_element_by_css_selector('#id_username')
        username_input.send_keys("victor@gmail.fr")
        password_input = self.browser.find_element_by_css_selector('#id_password')
        password_input.send_keys("blabla75")
        self.browser.find_element_by_id('confirmer').click()
        self.browser.find_element_by_xpath('//*[@id="page"]/div[2]/header/div/div/div[2]/div/form/input').send_keys('camembert lait cru')
        self.browser.find_element_by_xpath('//*[@id="page"]/div[2]/header/div/div/div[2]/div/form/button').click()
        print("assert 'Petit Camembert Au Lait Cru' in self.browser.page_source")
        assert 'Petit Camembert Au Lait Cru' in self.browser.page_source
        print('ASSERT DONE')

    def test_looking_for_non_existing_product(self):
        """
        User look for the product 'pâtes au ketchup' and see if a product exists matching the request.
        """
        self.browser.get(self.live_server_url)
        self.browser.maximize_window()
        self.browser.find_element_by_id('log in').click()
        username_input = self.browser.find_element_by_css_selector('#id_username')
        username_input.send_keys("victor@gmail.fr")
        password_input = self.browser.find_element_by_css_selector('#id_password')
        password_input.send_keys("blabla75")
        self.browser.find_element_by_id('confirmer').click()
        self.browser.find_element_by_xpath('//*[@id="page"]/div[2]/header/div/div/div[2]/div/form/input').send_keys('pâtes au ketchup')
        self.browser.find_element_by_xpath('//*[@id="page"]/div[2]/header/div/div/div[2]/div/form/button').click()
        print("assert 'Pas de produit à afficher' in self.browser.page_source")
        assert 'Pas de produit à afficher' in self.browser.page_source
        print('ASSERT DONE')
