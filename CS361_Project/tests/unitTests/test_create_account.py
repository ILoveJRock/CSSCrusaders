from django.test import TestCase, Client
from CS361_Project.models import Account

class TestAddAccount(TestCase):
  client = None
  accounts = None

  def setUp(self):
    self.client = Client()
    self.accounts = [
      {
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
    resp = self.client.post("/manage/createAccount/", {
      "name": "joe",
      "phone": "414",
      "email": "@hotmail",
      "address": "lane",
      "password": "123",
      "acctype": 1
    }, follow=True)
    self.assertEqual(1, len(Account.objects.filter(username="joe")), "The account was not created")

  def test_same_name(self):
    resp = self.client.post("/manage/createAccount/", {
      "name": "Joe Shmo",
      "phone": "555",
      "email": "@hotmail",
      "address": "lane",
      "password": "123",
      "acctype": 1
    }, follow=True)
    self.assertEqual(0, len(Account.objects.filter(phone="555")), "The account was incorrectly created")
    self.assertEqual("There is already an account with that username.", resp.context["message"], "The error message didn't show up")
