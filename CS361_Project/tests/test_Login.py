from unittest.mock import MagicMock

from django.test import TestCase, Client

from CS361_Project.models import Account


class LoginTests(TestCase):
    client = None

    def setUp(self):
        self.client = Client()
        
        account = Account(account_id=1, username="Joe", password="12345", role=0, name="Joe Schmo")
        account.save()

    def test_UserDoesNotExist(self):
        response = self.client.post('/login/', {'username': 'Bob', 'password': "12345"}, follow=True)
        # When the user doesn't exist the response should contain the error 'User does not exist'
        self.assertContains(response, 'User does not exist')
    def test_IncorrectPassword(self):
        response = self.client.post('/login/', {'username': 'Joe', 'password': "12346"}, follow=True)
        # When the incorrect password is submitted the response should contain the error 'Incorrect Password'
        self.assertContains(response, 'Incorrect Password')
    def test_AlreadyLoggedIn(self):
        session = self.client.session
        session['LoggedIn'] = True
        session['name'] = 'Joe Schmo'
        session['role'] = 0
        response = self.client.get('/login/', follow=True)
        self.assertRedirects(response, '/dashboard/')
        
        
    def test_SuccessfulLogin(self):
        response = self.client.post('/login/', {'username': 'Joe', 'password': "12345"}, follow=True)
        # Redirects to home when user is logged in
        self.assertRedirects(response, '/dashboard/')
        # When login is successful, we can check the name and role of the user to display the information on the dashboard
        session = self.client.session
        self.assertEqual(session['name'], "Joe Schmo")
        self.assertEqual(session['role'], 0)

        # When logged in, the state variable
        self.assertTrue(session['LoggedIn'])
