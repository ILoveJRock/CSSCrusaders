from unittest.mock import MagicMock

from django.test import TestCase, Client

from CS361_Project.models import Account


class EditAccountTests(TestCase):
    client = None

    def setUp(self):
        self.client = Client()
        account = Account(account_id=1, username="Joe", password="12345", role=0, name="Joe Schmo")
        account.save()

class DeleteAccountTests(TestCase):
    client = None

    def setUp(self):
        self.client = Client()
        account = Account(account_id=1, username="Joe", password="12345", role=0, name="Joe Schmo")
        account.save()