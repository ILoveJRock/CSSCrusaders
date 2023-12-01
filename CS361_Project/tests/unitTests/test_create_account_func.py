from django.test import TestCase
from unittest.mock import Mock
from funcs_for_views import create_account
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
    self.assertEqual(1, len(Account.objects.filter(username="joe")), "Too many accounts were created")
