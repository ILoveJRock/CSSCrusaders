from unittest.mock import MagicMock

from django.test import TestCase, Client

from CS361_Project.models import Account


class LogoutTests(TestCase):
    client = None

    def setUp(self):
        self.client = Client()
        account = Account(account_id=1, username="Joe", password="12345", role=0, name="Joe Schmo")
        account.save()
    def test_SuccessfulLogout(self):
        login_response = self.client.post('/login/', {'username': 'Joe', 'password': '12345'})
        self.assertEqual(login_response.status_code, 302)  # Assuming successful login redirects

        # Now, test the logout
        logout_response = self.client.get('/logout/')
        self.assertEqual(logout_response.status_code, 302)  # Assuming successful logout redirects
        self.assertRedirects(logout_response, '/login/')  # Assuming the user is redirected to the login page

        # Check if session data is cleared
        self.assertEqual(self.client.session.get('LoggedIn'), None)
        self.assertEqual(self.client.session.get('name'), None)
        self.assertEqual(self.client.session.get('role'), None)
