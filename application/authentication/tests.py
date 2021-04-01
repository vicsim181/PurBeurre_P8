from django import test
from django.http import request
from django.test import TestCase, Client
from .models import CustomUserManager, User


# Create your tests here.
class RegisterTest(TestCase):
    """
    Test functions of the registration functionality.
    """
    def setUp(self):
        test_user = User(email='essai@gmail.com', password=None, first_name='essai', last_name='REGISTER')
        test_user.set_password('blabla75')
        test_user.save()

    def test_user_created(self):
        print("\nTEST - User --> Register\n")
        user_test = User.objects.get(email='essai@gmail.com')
        print("self.assertEqual(user_test.first_name, 'essai')")
        self.assertEqual(user_test.first_name, 'essai')
        print("Assert Done")

    def test_str_(self):
        print("\nTEST - User --> __str__()\n")
        user_test = User.objects.get(email='essai@gmail.com')
        print("self.assertEqual(user_test, 'essai REGISTER essai@gmail.com')")
        self.assertEqual(str(user_test), 'essai REGISTER essai@gmail.com')
        print("Assert Done")

    def test_get_full_name(self):
        print("\nTEST - User --> get_full_name\n")
        user_test = User.objects.get(email='essai@gmail.com')
        print("self.assertEqual(user_test.get_full_name(), 'essai REGISTER')")
        self.assertEqual(user_test.get_full_name(), 'essai REGISTER')
        print("Assert Done")

    def test_get_email(self):
        print("\nTEST - User --> get_email\n")
        user_test = User.objects.get(first_name='essai', last_name='REGISTER')
        print("self.assertEqual(user_test.get_email(), 'essai@gmail.com')")
        self.assertEqual(user_test.get_email(), 'essai@gmail.com')
        print("Assert Done")


# class CustomeUserManagerTest(TestCase):
#     """
#     Testing the custom user manager created in the authentication models.
#     """
#     def test_create_user(self):
#         """
#         Test the create_user function of the custom user manager.
#         """
#         test_custom = CustomUserManager()
#         test_custom.create_user(self, 'essai@gmail.fr', 'essai+123!', 'essai123', 'USER')
#         user_test = User.objects.get(email='essai@gmail.fr')
#         print("self.assertEqual(user_test.first_name, 'essai123')")
#         self.assertEqual(user_test.first_name, 'essai123')
#         print("Assert Done")
        #  Result when testing:
        #         ERROR: test_create_user (authentication.tests.CustomeUserManagerTest)
        # ----------------------------------------------------------------------
        # Traceback (most recent call last):
        #   File "D:\onedrive\formation opcr\p8\github\application\authentication\tests.py", line 51, in test_create_user
        #     test_custom.create_user(self, 'essai@gmail.fr', 'essai+123!', 'essai123', 'USER')
        #   File "D:\onedrive\formation opcr\p8\github\application\authentication\models.py", line 17, in create_user
        #     user_obj = self.model(email=self.normalize_email(email))
        #   File "D:\onedrive\formation opcr\p8\github\env\lib\site-packages\django\contrib\auth\base_user.py", line 26, in normalize_email
        #     email_name, domain_part = email.strip().rsplit('@', 1)
        # AttributeError: 'CustomeUserManagerTest' object has no attribute 'strip'
