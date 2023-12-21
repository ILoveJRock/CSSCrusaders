from django.test import TestCase
from unittest.mock import Mock
from CS361_Project.functions import *


class TestLogout(TestCase):
    def test_logout(self):
        mock_request = Mock()
        mock_request.session = {'name': 'user', 'role': 'admin', 'LoggedIn': True}

        # Call the logout method with the mock request
        Management.User.logout(mock_request)

        # Assert that the session variables are cleared
        self.assertEqual(mock_request.session, {'LoggedIn': False})