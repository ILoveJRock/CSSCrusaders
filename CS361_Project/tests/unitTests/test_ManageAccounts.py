from django.test import TestCase
from unittest.mock import Mock
from CS361_Project.functions import *
from CS361_Project.models import Account


class TestCreateAccount(TestCase):
    def test_new_account(self):
        mock_request = Mock()
        mock_request.POST = {
            "name": "joe",
            "phone": "414",
            "email": "@hotmail",
            "address": "lane",
            "password": "123",
            "acctype": 1
        }
        create_account(mock_request)
        self.assertEqual(1, len(Account.objects.filter(username="joe")), "The account was not created")

    def test_duplicate_account(self):
        mock_request = Mock()
        mock_request.POST = {
            "name": "joe",
            "phone": "414",
            "email": "@hotmail",
            "address": "lane",
            "password": "123",
            "acctype": 1
        }
        create_account(mock_request)
        create_account(mock_request)
        self.assertEqual(1, len(Account.objects.filter(username="joe")), "Duplicate accounts are not allowed")


class TestEditAccount(TestCase):
    def setUp(self):
        # Create a mock instance of YourAccountModel
        self.mock_existingAccount = Mock()

        # Manually assign attributes to the mock instance
        self.mock_existingAccount.username = "existing_username"
        self.mock_existingAccount.password = "existing_password"
        self.mock_existingAccount.role = 1
        self.mock_existingAccount.name = "existing_name"
        self.mock_existingAccount.phone = "existing_phone"
        self.mock_existingAccount.email = "existing_email@example.com"
        self.mock_existingAccount.address = "existing_address"
        self.mock_existingAccount.office_hour_location = "existing_office_location"
        self.mock_existingAccount.office_hour_time = "existing_office_time"

        # Create a mock request with POST data
        self.mock_request = Mock()
        self.mock_request.POST = {
            "username": "joe",
            "password": "123",
            "role": "user",
            "name": "Joe",
            "phone": "414",
            "email": "joe@hotmail.com",
            "address": "Lane",
            "office_hour_location": "Office",
            "office_hour_time": "9 AM - 5 PM",
        }

    def test_EditAccount(self):
        # Call the updateAccount method with the mock request and account
        updateAccount(self.mock_request, self.mock_existingAccount)

        # Assert that the fields of mock_existingAccount have not changed
        self.assertEqual(self.mock_existingAccount.username, "joe")
        self.assertEqual(self.mock_existingAccount.password, "123")
        self.assertEqual(self.mock_existingAccount.role, "user")
        self.assertEqual(self.mock_existingAccount.name, "Joe")
        self.assertEqual(self.mock_existingAccount.phone, "414")
        self.assertEqual(self.mock_existingAccount.email, "joe@hotmail.com")
        self.assertEqual(self.mock_existingAccount.address, "Lane")
        self.assertEqual(self.mock_existingAccount.office_hour_location, "Office")
        self.assertEqual(self.mock_existingAccount.office_hour_time, "9 AM - 5 PM")

    def test_emptyPOSTData(self):
        # Create a test case where POST data is empty
        self.mock_request.POST = {}
        updateAccount(self.mock_request, self.mock_existingAccount)

        # Assert that mock_existingAccount remains unchanged
        self.assertEqual(self.mock_existingAccount.username, "existing_username")
        self.assertEqual(self.mock_existingAccount.password, "existing_password")
        self.assertEqual(self.mock_existingAccount.role, 1)
        self.assertEqual(self.mock_existingAccount.name, "existing_name")
        self.assertEqual(self.mock_existingAccount.phone, "existing_phone")
        self.assertEqual(self.mock_existingAccount.email, "existing_email@example.com")
        self.assertEqual(self.mock_existingAccount.address, "existing_address")
        self.assertEqual(self.mock_existingAccount.office_hour_location, "existing_office_location")
        self.assertEqual(self.mock_existingAccount.office_hour_time, "existing_office_time")

    def test_invalidPOSTData(self):
        # Create a test case with invalid POST data
        self.mock_request.POST = {
            "username": "newJoe",
            "password": "123",
            "role": "invalid_role",  # Invalid role format
            "name": "Joe",
            "phone": "invalid_phone",  # Invalid phone format
            "email": "invalid_email",  # Invalid email format
            "address": "Lane",
            "office_hour_location": "Office",
            "office_hour_time": "9 AM - 5 PM",
        }
        updateAccount(self.mock_request, self.mock_existingAccount)

        # Assert that mock_existingAccount remains unchanged or is handled appropriately
        self.assertEqual(self.mock_existingAccount.username, "existing_username")
        self.assertEqual(self.mock_existingAccount.password, "existing_password")
        self.assertEqual(self.mock_existingAccount.role, 1)
        self.assertEqual(self.mock_existingAccount.name, "existing_name")
        self.assertEqual(self.mock_existingAccount.phone, "existing_phone")
        self.assertEqual(self.mock_existingAccount.email, "existing_email@example.com")
        self.assertEqual(self.mock_existingAccount.address, "existing_address")
        self.assertEqual(self.mock_existingAccount.office_hour_location, "existing_office_location")
        self.assertEqual(self.mock_existingAccount.office_hour_time, "existing_office_time")


class TestDeleteAccount(TestCase):
    def setUp(self):
        # Create a mock instance of YourAccountModel
        self.mock_existingAccount = Mock()

        # Manually assign attributes to the mock instance
        self.mock_existingAccount.username = "existing_username"
        self.mock_existingAccount.password = "existing_password"
        self.mock_existingAccount.role = 1
        self.mock_existingAccount.name = "existing_name"
        self.mock_existingAccount.phone = "existing_phone"
        self.mock_existingAccount.email = "existing_email@example.com"
        self.mock_existingAccount.address = "existing_address"
        self.mock_existingAccount.office_hour_location = "existing_office_location"
        self.mock_existingAccount.office_hour_time = "existing_office_time"

    def test_DeleteAccount(self):
        # Call the deleteAccount method with the mock account
        deleteAccount(self.mock_existingAccount)

        # Assert that the account has been deleted
        self.assertFalse(Account.objects.filter(username="existing_username").exists(), "The account was not deleted")
