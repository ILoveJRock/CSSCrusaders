from django.test import TestCase, Client

from CS361_Project.models import Account


class LoginAcceptance(TestCase):
    # As any user, I need to be able to log in and out so that my data is secure from other users on the same computer
    client = None

    def setUp(self):
        self.client = Client()
        self.account = Account.objects.create(account_id=1, username="Joe", password="12345", role=0, name="Joe Schmo")
        self.account.save()

    def test_criteriaOne(self):
        # GIVEN no one is logged in
        self.client.post('/logout/', follow=True)
        # WHEN a user enters a username and password that matches a pair in the database
        response = self.client.post('/login/', {'username': 'Joe', 'password': '12345'}, follow=True)

        # THEN they are redirected to the home page logged in as that user
        self.assertRedirects(response, '/')
        self.assertTrue(response.context['LoggedIn'])
        self.assertEqual(response.context['name'], 'Joe Schmo')
        self.assertEqual(response.context['role'], 0)

    def test_criteriaTwo(self):
        # GIVEN no one is logged in
        self.client.post('/logout/', follow=True)
        # WHEN a user enters a username and password pair not in the database
        response = self.client.post('/login/', {'username': 'InvalidUser', 'password': 'InvalidPassword'}, follow=True)

        # THEN they stay on the login page and an error is displayed
        self.assertContains(response, 'User does not exist')
        self.assertFalse(response.context['LoggedIn'])  # Assuming it's False for a failed login

    def test_criteriaThree(self):
        # GIVEN a user is logged in
        # TODO ???
        # WHEN they select the log out button
        response = self.client.get('/logout/', follow=True)

        # THEN they are redirected to the login page and are no longer logged in
        self.assertRedirects(response, '/login/')
        self.assertFalse(response.context['LoggedIn'])


class CreateAccountAcceptance(TestCase):
    # As a supervisor or administrator, I need to be able to create instructor and TA accounts so that random people can’t get in the system.
    client = None

    def setUp(self):
        self.client = Client()
        self.account = Account.objects.create(account_id=1, username="Joe", password="12345", role=0, name="Joe Schmo")
        self.account.save()

    def test_criteriaOne(self):
        # GIVEN a user already exists with a certain username
        existing_account = self.account
        old_num_accounts = Account.objects.count()

        # WHEN an admin attempts to create an account with that name
        response = self.client.post('manage/createAccount/',
                                    {'name': 'Joe', 'phone': '1234567890', 'email': 'new@example.com',
                                     'address': 'New Address', 'password': 'new_password', 'acctype': 'instructor'})
        # THEN no change happens to the database
        self.assertEqual(Account.objects.count(), old_num_accounts)
        # AND the admin sees a message that the account already exists
        self.assertContains(response, 'There is already an account with that username.')

    def test_criteriaTwo(self):
        # GIVEN an account with a certain username doesn’t exist yet

        # WHEN an admin attempts to create that account
        response = self.client.post('manage/createAccount/',
                                    {'name': 'NewUser', 'phone': '1234567890', 'email': 'new@example.com',
                                     'address': 'New Address', 'password': 'new_password', 'acctype': 'instructor'}, follow=True)
        # Check if the request was successful (status code 200 OK)
        self.assertEqual(response.status_code, 200)

        # THEN the account is created in the database with no assigned course or information
        new_account = Account.objects.get(username='NewUser')
        self.assertEqual(new_account.role, 1)

        # AND the account can be logged into from another computer
        response = self.client.post('/login/', {'username' : 'NewUser', 'password' : 'new_password'}, follow=True)

        session = response.session
        self.assertEqual(session['name'], "NewUser")
        self.assertEqual(session['role'], 1)
        self.assertTrue(session['LoggedIn'])
