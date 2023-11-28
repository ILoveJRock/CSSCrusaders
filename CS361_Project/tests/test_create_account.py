from django.test import TestCase, Client
from CS361_Project.models import Account

class TestAddAccount(TestCase):
  client = None
  accounts = None

  def setUp(self):
    self.client = Client()
    self.accounts = [
      {
        "id": 1,
        "username": "Joe Shmo",
        "password": "123",
        "role": 1,
        "name": "Joe Shmo",
        "phone": "414",
        "email": "@gmail",
        "address": "street"
      }
    ]

    for i in self.accounts:
      account = Account(
        account_id=i["id"],
        username=i["username"],
        password=i["password"],
        role=i["role"],
        name=i["name"],
        phone=i["phone"],
        email=i["email"],
        address=i["address"]
      )
      account.save()

  def test_new_account(self):
    resp = self.client.post("manage/createAccount/", {
      "id": 2,
      "name": "joe",
      "phone": "414",
      "email": "@hotmail",
      "address": "lane",
      "password": "123",
      "acctype": 1
    }, follow=True)
    self.assertEqual(1, len(Account.objects.filter(account_id=2)), "The account was not created")