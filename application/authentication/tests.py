from django import test
from django.http import request
from django.test import TestCase, Client
from .models import User
# User = get_user_model()


# Create your tests here.
class RegisterTest(TestCase):
    """
    Test functions of the registration functionality.
    """
    def setUp(self):
        test_user = User(email='essai@gmail.com', password=None, first_name='essai', last_name='register')
        test_user.set_password('blabla75')
        test_user.save()

    def test_user_created(self):
        print("\nTEST - User --> Register\n")
        user_test = User.objects.get(email='essai@gmail.com')
        print("self.assertEqual(user_test.first_name, 'essai')")
        self.assertEqual(user_test.first_name, 'essai')
        print("Assert Done")


class LoginLogoutTest(TestCase):
    """
    Test functions of the Login and Logout functionality.
    """
    def setUp(self):
        self.test_user = User(email='essai@gmail.com', password=None, first_name='essai', last_name='register')
        self.test_user.set_password('blabla75')
        self.test_user.save()

    def test_login(self):
        print("\nTEST - User --> Login\n")
        # c = Client()
        login_result = self.client.login(email='essai@gmail.com', password='blabla75')
        print("self.assertTrue(essai@gmail.com is authenticated)")
        self.assertTrue(login_result)
        print('Assert 1 Done')
        login_result = self.client.login(email='essai2@gmail.com', password='blabla75')
        print("self.assertFalse(essai2@gmail.com is authenticated)")
        self.assertFalse(login_result)
        print('Assert 2 Done')

    # def test_logout(self):
        # logout_response = self.client.get('user/logout/')
        # print('ESSAI: ' + str(logout_response))
        # print('LOGOUT ' + str(logout_result))
        # print("self.assertEqual(essai@gmail.com is authenticated, False)")
        # self.assertFalse(self.test_user.is_authenticated)
        # print('Assert 2 Done')
        # print("self.assertEqual(essai@gmail.com is logged in, False)")
        # self.assertEqual(logged_in, False)
        # print('Assert 3 Done')
