from unittest.mock import MagicMock

from django.test import TestCase, Client

from CS361_Project.models import Account


class EditAccountTests(TestCase):
    client = None

    def setUp(self):
        self.client = Client()
        self.account = Account(username="Joe",
                               password="12345",
                               role=0,
                               name="Joe Schmo",
                               phone='1234567890',
                               email='example@gmail.com',
                               address='Test Address',
                               office_hour_location='Office Location',
                               office_hour_time='Office Hours', )
        self.account.save()

    def test_changesMade(self):
        # Test if changes are successfully made to the user account
        updated_data = {
            'username': 'NewUsername',
            'password': 'NewPassword',
            'role': 1,  # Assuming 1 corresponds to 'Instructor' in your model
            'phone': '9876543210',
            'name' : 'New Name',
            'email': 'new@example.com',
            'address': 'New Address',
            'office_hour_location': 'New Location',
            'office_hour_time': 'New Hours',
        }

        # Ensure the account exists with the initial data
        self.assertEqual(self.account.username, 'Joe')

        # When a new post request with updated data is submitted...
        response = self.client.post(f'/manage/editAccount/?userId={self.account.account_id}', {'userId': self.account.account_id, **updated_data})
        # The account information should change accordingly
        updated_user = Account.objects.get(account_id=self.account.account_id)
        # Assert that the account information has been updated to match updated_data
        self.assertEqual(updated_user.username, updated_data['username'])
        self.assertEqual(updated_user.password, updated_data['password'])
        self.assertEqual(updated_user.role, updated_data['role'])
        self.assertEqual(updated_user.name, updated_data['name'])
        self.assertEqual(updated_user.phone, updated_data['phone'])
        self.assertEqual(updated_user.email, updated_data['email'])
        self.assertEqual(updated_user.address, updated_data['address'])
        self.assertEqual(updated_user.office_hour_location, updated_data['office_hour_location'])
        self.assertEqual(updated_user.office_hour_time, updated_data['office_hour_time'])

        # After changes are made, the user should be redirected to the ManageAccount view
        self.assertRedirects(response, '/manage/')


    def test_emptyLogin(self):
        bad_data = {
            'username': '',  # Empty username should be invalid
            'password': '',  # Empty password should be invalid
        }
        # When a new post request with bad data is submitted...
        response = self.client.post(f'/manage/editAccount/?userId={self.account.account_id}',
                                    {'userId': self.account.account_id, **bad_data})
        # The form is re-rendered with errors
        self.assertContains(response, 'Login fields cannot be empty')  # Check for a required field error

    def test_usernameTaken(self):
        # Test if the form submission fails when trying to change to an existing username
        existing_username = 'ExistingUser'
        existing_account = Account.objects.create(
            username=existing_username,
            password='12345',
            role=0,
            name="Existing User",
            phone='1234567890',
            email='existing@example.com',
            address='Existing Address',
            office_hour_location='Existing Location',
            office_hour_time='Existing Hours',
        )
        existing_account.save()

        new_data = {
            'username' : existing_username,
            'password' : "12345",
            'role' : 0,
            'name' : "Joe Schmo",
            'phone' : '1234567890',
            'email' : 'example@gmail.com',
            'address' : 'Test Address',
            'office_hour_location' : 'Office Location',
            'office_hour_time' : 'Office Hours'
        }

        # When a new post request with a taken username is submitted...
        response = self.client.post(f'/manage/editAccount/?userId={self.account.account_id}',
                                    {'userId': self.account.account_id, **new_data})

        # Check if the form is re-rendered with a username taken error
        self.assertContains(response, 'An account with that username already exists.')

    def test_nonexistentUser(self):
        # Test if the view handles a request for a nonexistent user ID
        invalid_user_id = 999999999 # assuming this is not in the database

        with self.assertRaises(Account.DoesNotExist):
            # Send a POST request to the editAccount view with an invalid user ID
            # Follow the redirects to handle any redirects (e.g., to an error page)
            self.client.post(
                f'/manage/editAccount/?userId={self.account.account_id}',
                {'userId': invalid_user_id},
                follow=True
            )