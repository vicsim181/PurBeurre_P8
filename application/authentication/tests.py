from django.test import TestCase, RequestFactory
from django.urls.base import reverse
from .models import User
from .views import RegisterView, ConsultAccountView
from .forms import RegisterForm
from unittest import mock
from unittest.mock import patch, MagicMock


# Create your tests here.
class RegisterTest(TestCase):
    """
    Test functions of the registration functionality.
    """
    def setUp(self):
        self.user_test = User(email='essai@gmail.com', password=None, first_name='essai', last_name='REGISTER')
        self.user_test.set_password('blabla75')
        self.user_test.save()

    def test_user_created(self):
        print("\nTEST - User --> Register\n")
        user_test = User.objects.get(email='essai@gmail.com')
        print("self.assertEqual(user_test.first_name, 'essai')")
        self.assertEqual(user_test.first_name, 'essai')
        print("Assert Done")

    def test_str_(self):
        print("\nTEST - User --> __str__()\n")
        print("self.assertEqual(self.user_test, 'essai REGISTER essai@gmail.com')")
        self.assertEqual(str(self.user_test), 'essai REGISTER essai@gmail.com')
        print("Assert Done")

    def test_get_full_name(self):
        print("\nTEST - User --> get_full_name()\n")
        print("self.assertEqual(self.user_test.get_full_name(), 'essai REGISTER')")
        self.assertEqual(self.user_test.get_full_name(), 'essai REGISTER')
        print("Assert Done")

    def test_get_email(self):
        print("\nTEST - User --> get_email()\n")
        print("self.assertEqual(user_test.get_email(), 'essai@gmail.com')")
        self.assertEqual(self.user_test.get_email(), 'essai@gmail.com')
        print("Assert Done")

    def test_has_perm(self):
        print("\nTEST - User --> has_perm()\n")
        print("self.assertTrue(self.test_user.has_perm('view_product'))")
        self.assertTrue(self.user_test.has_perm('view_product'))
        print('ASSERT DONE')


# @patch.object(RegisterView.post, 'form', autospec=RegisterForm)
class TestRegisterView(TestCase):
    """
    Test class for AuthenticationView.
    """
    def setUp(self):
        self.factory = RequestFactory()

    def test_registerview_get(self):
        print("\nTEST - REGISTERVIEW --> def get()\n")
        request = self.factory.get('register/', )
        response = RegisterView.as_view()(request)
        print("self.assertEqual(response.status_code, 200)")
        self.assertEqual(response.status_code, 200)
        print('Assert Done')

    def test_registerview_post(self):
        print("\nTEST - REGISTERVIEW --> def post()\n")
        with mock.patch('views.RegisterForm.is_valid') as mocked_form:
            mocked_form.return_value = True
            request = self.factory.post(reverse('register'), data={})
            response = RegisterView.as_view()(request)
            self.assertEqual(response.status_code, 200)


class TestConsultAccountView(TestCase):
    """
    Test class for ConsultAccountView.
    """
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='test',
                                             email='essai123@gmail.fr',
                                             password='lol175+essai')

    def test_consultaccountview_get(self):
        print("\nTEST - CONSULTACCOUNTVIEW --> def get()\n")
        request = self.factory.get('account/', )
        request.user = self.user
        response = ConsultAccountView.as_view()(request)
        print("self.assertEqual(response.status_code, 200)")
        self.assertEqual(response.status_code, 200)
        print('Assert Done')
