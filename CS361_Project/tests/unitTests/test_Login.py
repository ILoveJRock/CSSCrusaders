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
        
    def test_Login(self):
        mock_request = Mock()
        mock_request.POST = {
            "username": "username",
            "password": "password",
            'LoggedIn' : False
        }
        Management.User.login(mock_request, self.mock_user)
        
        # Assert that session variables are set correctly
        self.assertEqual(mock_request.session['name'], self.mock_user.name)
        self.assertEqual(mock_request.session['role'], self.mock_user.role)
        self.assertTrue(mock_request.session['LoggedIn'])
    def test_authenticate_user(self):
         mock_user = Mock()
         mock_user.username = "test_user"
         mock_user.password = "test_password"
         #TODO: not sure if this is even correct, any other way to mock an account that will show in get?
         Account.objects.get = Mock(return_value=mock_user)

         # Test authentication with valid credentials
         result = Management.User.authenticate_user(mock_user.username, mock_user.password)

         # Assert that the correct user is returned
         self.assertEqual(result, mock_user)
        
# TODO: After main merge with fixed logout
class TestLogout(TestCase):
    def test_logout():
        pass