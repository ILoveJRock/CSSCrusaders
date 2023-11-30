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

        # WHEN they select the log out button
        response = self.client.get('/logout/', follow=True)

        # THEN they are redirected to the login page and are no longer logged in
        self.assertRedirects(response, '/login/')
        self.assertFalse(response.context['LoggedIn'])
        session = self.client.session
        self.assertNotIn('name', session)
        self.assertNotIn('role', session)
        self.assertFalse(session['LoggedIn'])


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
        response = self.client.post('/manage/createAccount/',
                                    {'name': 'Joe', 'phone': '1234567890', 'email': 'new@example.com',
                                     'address': 'New Address', 'password': 'new_password', 'acctype': 'instructor'})
        # THEN no change happens to the database
        self.assertEqual(Account.objects.count(), old_num_accounts)
        # AND the admin sees a message that the account already exists
        self.assertContains(response, 'There is already an account with that username.')

    def test_criteriaTwo(self):
        # GIVEN an account with a certain username doesn’t exist yet

        # WHEN an admin attempts to create that account
        response = self.client.post('/manage/createAccount/',
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

class DeleteAccountAcceptance(TestCase):
    # As a supervisor or administrator, I want to be able to delete accounts so that if someone leaves UWM they don’t stay in the system.
    client = None

    def setUp(self):
        self.client = Client()
        self.account = Account.objects.create(account_id=1, username="Joe", password="12345", role=0, name="Joe Schmo")
        self.accountToDelete  = Accounts.objects.create(account_id=2, username="Bob", password="12345", role=1, name="Bob B.")
        self.accountToDelete.save()
        self.account.save()

    def test_criteriaOne(self):
        # GIVEN the admin is on the page with all accounts
        response = self.client.get('/manage/', follow=True)
        # WHEN they click on an account
        account_id_to_delete = self.accountToDelete.account_id
        # THEN there is an option to delete it
        response = self.client.post(f'/manage/deleteAccount?userId={account_id_to_delete}', follow=True)

        self.assertContains(response, 'Delete Account')
        # AND the admin is prompted to confirm the deletion if they select that option
class EditAccountAcceptance(TestCase):
    # As a supervisor or administrator, I want to be able to edit the information on other accounts
    # so that if someone enters the wrong information it is quickly corrected.
    client = None

    def setUp(self):
        self.client = Client()
        self.account = Account.objects.create(account_id=1, username="Joe", password="12345", role=0, name="Joe Schmo")
        self.account.save()

    def test_criteriaOne(self):
        # GIVEN the admin is on the page with all accounts
        # WHEN they click on an account
        # THEN there is an option to edit the account’s information
        pass

    def test_criteriaTwo(self):
        # GIVEN the admin has entered new information for the account
        response = self.client.post('/manage//editAccount/', {'username': 'Joe', 'new_field': 'new_value'}, follow=True)

        # WHEN they press the submit button
        self.assertEqual(response.status_code, 200)

        # THEN the account is updated in the database
        updated_account = Account.objects.get(username='Joe')
        self.assertEqual(updated_account.new_field, 'new_value')

        # AND the admin sees a confirmation message
        self.assertContains(response, 'Account information updated successfully.')

    def test_criteriaThree(self):
        # GIVEN the admin entered the same information the account already has
        response = self.client.post('/edit_account/', {'username': 'Joe', 'new_field': 'existing_value'}, follow=True)

        # WHEN they press the submit button
        self.assertEqual(response.status_code, 200)

        # THEN they see a message saying that there were no changes made
        self.assertContains(response, 'No changes were made to the account information.')

    def test_criteriaFour(self):
        # GIVEN at least one field is blank in the page to change account information
        response = self.client.post('/edit_account/', {'username': 'Joe', 'new_field': ''}, follow=True)

        # WHEN the admin presses the submit button
        self.assertEqual(response.status_code, 200)

        # THEN the database is not updated
        unchanged_account = Account.objects.get(username='Joe')
        self.assertEqual(unchanged_account.new_field, 'existing_value')

        # AND they see a message saying that they need to enter information
        self.assertContains(response, 'Please enter information for all fields.')


