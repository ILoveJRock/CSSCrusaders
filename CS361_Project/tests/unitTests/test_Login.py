from django.test import TestCase
from unittest.mock import Mock
from CS361_Project.functions import *
from CS361_Project.models import Account


class TestLogin(TestCase):
    def setUp(self):
        self.mock_user = Mock()
        self.mock_user.username = 'username'
        self.mock_user.password = 'password'
        self.mock_user.name = 'name'
        self.mock_user.role = 1
        self.mock_request = Mock()
        self.mock_request.POST = {
            "username": "username",
            "password": "password",
            'LoggedIn': False
        }
        self.mock_request.session = {}

    def test_Login(self):

        Management.User.login(self.mock_request, self.mock_user)
        
        # Assert that session variables are set correctly
        self.assertEqual(self.mock_request.session['name'], self.mock_user.name)
        self.assertEqual(self.mock_request.session['role'], self.mock_user.role)
        self.assertTrue(self.mock_request.session['LoggedIn'])
    def test_authenticate_user(self):
        mock_user = Mock()
        mock_user.username = "test_user"
        mock_user.password = "test_password"

        Account.objects.get = Mock(return_value=mock_user)

        # Test authentication with valid credentials
        result = Management.User.authenticate_user(mock_user.username, mock_user.password)

        # Assert that the correct user is returned
        self.assertEqual(result, mock_user)
        
# TODO: After main merge with fixed logout
class TestLogout(TestCase):
    def test_logout(self):
        pass