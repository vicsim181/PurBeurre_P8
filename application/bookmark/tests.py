from .models import Substitution
from .views import BookmarksView
from authentication.models import User
# from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import RequestFactory, TestCase
from main.models import Product
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.firefox.webdriver import WebDriver
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By


# Create your tests here.
class BookmarkTests(TestCase):
    """
    Test class holding the functions testing the Substitution model.
    """
    def setUp(self):
        self.product_source = Product(name="Coca-Cola Classic",
                                      code="5449000000996",
                                      nutriscore="e",
                                      url="https://fr.openfoodfacts.org/produit/5449000000996/coca-cola",
                                      popularity=2802)
        self.product_source.save()
        self.product_target = Product(name="Coca-Cola Zero",
                                      code="5449000133335",
                                      nutriscore="b",
                                      url="https://fr.openfoodfacts.org/produit/5449000133335/coca-cola-zero",
                                      popularity=181)
        self.product_target.save()
        test_user = User(email='essai@gmail.com', password=None, first_name='essai', last_name='register')
        test_user.set_password('blabla75')
        test_user.save()
        self.target_user = User.objects.get(email='essai@gmail.com')

    def test_save_and_get_bookmarks(self):
        print("\nTEST - Bookmark --> def save_bookmark()\n")
        Substitution.save_bookmark(self.product_source.id, self.product_target.id, self.target_user.id)
        print("TEST_BOOKMARK SAVED")
        print("\nTEST - Bookmark --> def get_bookmarks()\n")
        test_get_bookmarks = Substitution.get_bookmarks_by_user(self.target_user.id)
        print("self.assertTrue(test_get_bookmarks[0].target_product_id, self.product_target.id)")
        self.assertTrue(test_get_bookmarks[0].target_product_id, self.product_target.id)
        print('Assert 1 Done')
        print("self.assertTrue(test_get_bookmarks[0].source_product_id, self.product_source.id)")
        self.assertTrue(test_get_bookmarks[0].source_product_id, self.product_source.id)
        print('Assert 2 Done')

    def test_get_and_delete_bookmark(self):
        print("\nTEST - Bookmark --> def delete_bookmark()\n")
        Substitution.save_bookmark(self.product_source.id, self.product_target.id, self.target_user.id)
        print("TEST_BOOKMARK SAVED")
        test_delete_bookmark = Substitution.objects.get(
                               source_product_id=self.product_source.id,
                               target_product_id=self.product_target.id,
                               user_id=self.target_user.id)
        print("test_delete_bookmark.delete()")
        test_delete_bookmark.delete()
        print("\ndef get_bookmarks_by_user()\n")
        test_get_bookmarks = Substitution.get_bookmarks_by_user(self.target_user.id)
        print("self.assertQuerysetEqual(test_get_bookmarks, [])")
        self.assertQuerysetEqual(test_get_bookmarks, [])
        print('Assert 1 Done')

    def test_specific_bookmark(self):
        print("\nTEST - Bookmark --> def specific_bookmark()\n")
        Substitution.save_bookmark(self.product_source.id, self.product_target.id, self.target_user.id)
        test_specific_1 = Substitution.specific_bookmark(self.product_source.id, self.product_target.id,
                                                         self.target_user.id)
        print("self.assertTrue(Substitution.specific_bookmark(self.product_source.id, self.product_target.id,\
 self.target_user.id))")
        self.assertTrue(test_specific_1)
        print('ASSERT 1 DONE')
        print("self.assertFalse(Substitution.specific_bookmark(5620, 5621, 12))")
        test_specific_2 = Substitution.specific_bookmark(5620, 5621, 12)
        self.assertFalse(test_specific_2)
        print("ASSERT 2 DONE")

    def test_check_favs(self):
        print("\nTEST - Bookmark --> def check_favs()\n")
        Substitution.save_bookmark(self.product_source.id, self.product_target.id, self.target_user.id)
        test_favs = Substitution.check_favs(self.product_source, self.target_user)
        print('test_favs: ' + str(test_favs))
        print("self.assertEqual(Substitution.check_favs(self.product_source, self.target_user)[0], 2")
        self.assertEqual(test_favs[0], 2)
        print('ASSERT DONE')


class TestBookmarksView(TestCase):
    """
    Test class for BookmarksView.
    """
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='test',
                                             email='essaitest@gmail.fr',
                                             password='essaimdp+88')
        product = Product(name="Coca cola 1L",
                          code="5449000054227",
                          nutriscore="e",
                          url="https://fr.openfoodfacts.org/produit/5449000054227/coca-cola",
                          popularity=561,)
        product.save()
        product = Product(name="Coca Zéro",
                          code="5449000133328",
                          nutriscore="b",
                          url="https://fr.openfoodfacts.org/produit/5449000133328/coca-zero-coca-cola",
                          popularity=538,)
        product.save()

    def test_bookmarksview_get(self):
        print("\nTEST - BOOKMARKSVIEW --> def get()\n")
        substitution = Substitution(source_product_id=Product.objects.get(code="5449000133328").id,
                                    target_product_id=Product.objects.get(code="5449000054227").id,
                                    user_id=self.user.id,)
        substitution.save()
        request = self.factory.get('consult/', )
        request.user = self.user
        response = BookmarksView.as_view()(request)
        print("self.assertEqual(response.status_code, 200)")
        self.assertEqual(response.status_code, 200)
        print('Assert Done')

    def test_bookmarksview_post(self):
        print("\nTEST - BOOKMARKSVIEW --> def post() --> add bookmark\n")
        data = {
            'aim': 'add',
            'current_user': self.user,
            'product_id': 11,
            'suggestion_id': 12,
        }
        request = self.factory.post('consult/', data)
        request.user = self.user
        BookmarksView.as_view()(request)
        bookmark_test = Substitution.objects.get(user_id=self.user.id)
        print("self.assertEqual(bookmark_test.source_product_id, 11)")
        self.assertEqual(bookmark_test.source_product_id, 11)
        print("ASSERT DONE")
        print("\nTEST - BOOKMARKSVIEW --> def post() --> delete bookmark\n")
        data = {
            'aim': 'delete',
            'current_user': self.user,
            'product_id': 11,
            'suggestion_id': 12,
        }
        request = self.factory.post('consult/', data)
        request.user = self.user
        response = BookmarksView.as_view()(request)
        bookmark_test = Substitution.objects.all()
        print("self.assertIsNone(bookmark_test)")
        self.assertQuerysetEqual(bookmark_test, [])
        print("ASSERT DONE")
        print("self.assertEqual(response, 302)")
        self.assertEqual(response.status_code, 302)
        print("ASSERT DONE")
        print("\nTEST - BOOKMARKSVIEW --> def post() --> empty 'aim'\n")
        data = {
            'aim': '',
            'current_user': self.user,
            'product_id': 11,
            'suggestion_id': 12,
        }
        request = self.factory.post('consult/', data)
        request.user = self.user
        BookmarksView.as_view()(request)


# class UserStoriesBookmarkTest(StaticLiveServerTestCase):
#     """
#     Bookmark User stories:  user stories about searching a product.
#     Selenium is used to realise the following tests.
#     """
#     fixtures = ['users.json']

#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         cls.browser = WebDriver()
#         cls.browser.implicitly_wait(10)

#     @classmethod
#     def tearDownClass(cls):
#         cls.browser.quit()
#         super().tearDownClass()

#     def test_add_bookmark(self):
#         """
#         User story: A user logs in, search 'coca cola' and add the first result as a bookmark.
#         The user then checks its bookmarks.
#         """
#         self.browser.get(self.live_server_url)
#         self.browser.maximize_window()
#         self.browser.find_element_by_id('log in').click()
#         username_input = self.browser.find_element_by_css_selector('#id_username')
#         username_input.send_keys("victor@gmail.fr")
#         password_input = self.browser.find_element_by_css_selector('#id_password')
#         password_input.send_keys("blabla75")
#         self.browser.find_element_by_id('confirmer').click()
#         self.browser.find_element_by_xpath('//*[@id="page"]/div[2]/header/div/div/div[2]/div/form/input').send_keys('coca cola')
#         self.browser.find_element_by_xpath('//*[@id="page"]/div[2]/header/div/div/div[2]/div/form/button').click()
#         save_button = self.browser.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div[1]/form/button')
#         actions = ActionChains(self.browser)
#         actions.move_to_element(save_button)
#         actions.perform()
#         # ActionChains(self.browser).move_to_element(WebDriverWait(self.browser, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[1]/form/button")))).click().perform()
#         self.browser.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div[1]/form/button').click()
#         self.browser.find_element_by_xpath('/html/body/div[1]/div[1]/nav/div/ul[2]/li[2]/a').click()
#         print("assert 'Coca Cola remplacé par Coca-Cola Zéro' in self.browser.page_source")
#         assert 'Coca Cola remplacé par Coca-Cola Zéro' in self.browser.page_source
#         print('ASSERT DONE')


# Echec à déplacer la partie visible du site sur la première suggestion et cliquer sur le bouton sauvegarder.
# selenium.common.exceptions.ElementClickInterceptedException: Message: element click intercepted: Element <button type="submit" id="button">...</button> is not clickable at point (356, 948). Other element would receive the click: <a href="/mentionslegales/">...</a>
# Différentes solutions cherchées mais aucune ne fonctionne, ni sur Firefox ni sur Chrome
