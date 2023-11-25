from django.test import TestCase, Client
CS361_Project.models import Account

class TestAddItem(TestCase):
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
        id=i["id"],
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
    pass