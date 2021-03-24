from bookmark.models import Substitution
from django.test import TestCase
from authentication.models import User
from main.models import Product


# Create your tests here.
class BookmarkTests(TestCase):
    """
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
        test_get_bookmarks = Substitution.get_bookmarks(self.target_user.id)
        print("self.assertTrue(test_get_bookmarks[0].target_product_id, self.product_target.id)")
        self.assertTrue(test_get_bookmarks[0].target_product_id, self.product_target.id)
        print('Assert 1 Done')
        print("self.assertTrue(test_get_bookmarks[0].source_product_id, self.product_source.id)")
        self.assertTrue(test_get_bookmarks[0].source_product_id, self.product_source.id)
        print('Assert 2 Done')
