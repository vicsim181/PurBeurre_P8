from django import test
from bookmark.models import Substitution
from django.test import TestCase
from authentication.models import User
from main.models import Product


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
        test_specific_1 = Substitution.specific_bookmark(self.product_source.id, self.product_target.id, self.target_user.id)
        print("self.assertTrue(Substitution.specific_bookmark(self.product_source.id, self.product_target.id, self.target_user.id))")
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
