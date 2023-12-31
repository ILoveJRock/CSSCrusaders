from django.test import TestCase, Client

from CS361_Project.models import Account


class LoginAcceptance(TestCase):
    # As any user, I need to be able to log in and out so that my data is secure from other users on the same computer
    client = None

    def setUp(self):
        self.client = Client()
        self.account1 = Account.objects.create(
            account_id=1, username="Joe", password="12345", role=0, name="Joe Schmo"
        )
        self.account2 = Account.objects.create(
            account_id=2, username="Joel", password="12345", role=1, name="Joel Schmol"
        )
        self.account3 = Account.objects.create(
            account_id=3, username="Joey", password="12345", role=2, name="Joey Schmoey"
        )

        self.account1.save()
        self.account2.save()
        self.account3.save()

    def test_criteriaOne_Supervisor(self):
        # GIVEN no one is logged in
        session = self.client.session
        self.client.post("/logout/", follow=True)
        self.assertFalse(session.get("LoggedIn", False))

        # WHEN a user enters a username and password that matches a pair in the database
        response = self.client.post(
            "/login/", {"username": "Joe", "password": "12345"}, follow=True
        )

        # THEN they are redirected to the home page logged in as that user
        self.assertRedirects(response, "/dashboard/")

        response = self.client.get("/dashboard/")
        self.assertTrue(response.context["request"].session.get("LoggedIn", False))
        self.assertEqual(response.context["request"].session["name"], "Joe Schmo")
        self.assertEqual(response.context["request"].session["role"], 0)

    def test_criteriaOne_Instructor(self):
        # GIVEN no one is logged in
        session = self.client.session
        self.client.post("/logout/", follow=True)

        # WHEN a user enters a username and password that matches a pair in the database
        response = self.client.post(
            "/login/", {"username": "Joel", "password": "12345"}, follow=True
        )

        # THEN they are redirected to the home page logged in as that user
        self.assertRedirects(response, "/dashboard/prof/")

        # Follow the redirect to check session
        response = self.client.get("/dashboard/prof/")
        self.assertTrue(response.context["request"].session.get("LoggedIn", False))
        self.assertEqual(response.context["request"].session["name"], "Joel Schmol")
        self.assertEqual(response.context["request"].session["role"], 1)

    def test_criteriaOne_TA(self):
        # GIVEN no one is logged in
        session = self.client.session
        self.client.post("/logout/", follow=True)

        # WHEN a user enters a username and password that matches a pair in the database
        response = self.client.post(
            "/login/", {"username": "Joey", "password": "12345"}, follow=True
        )

        # THEN they are redirected to the home page logged in as that user
        self.assertRedirects(response, "/dashboard/ta/")

        # Follow the redirect to check session
        response = self.client.get("/dashboard/ta/")
        self.assertTrue(response.context["request"].session.get("LoggedIn", False))
        self.assertEqual(response.context["request"].session["name"], "Joey Schmoey")
        self.assertEqual(response.context["request"].session["role"], 2)

    def test_criteriaTwo(self):
        # GIVEN no one is logged in
        session = self.client.session
        self.client.post("/logout/", follow=True)

        # WHEN a user enters a username and password pair not in the database
        response = self.client.post(
            "/login/",
            {"username": "InvalidUser", "password": "InvalidPassword"},
            follow=True,
        )

        # THEN they stay on the login page and an error is displayed
        self.assertContains(response, "User does not exist")
        self.assertFalse(
            session.get("LoggedIn", False)
        )  # Assuming it's False for a failed login

    def test_criteriaThree(self):
        # GIVEN a user is logged in
        session = self.client.session
        self.client.post(
            "/login/", {"username": "Joe", "password": "12345"}, follow=True
        )

        # WHEN they select the log out button
        response = self.client.get("/logout/", follow=True)

        # THEN they are redirected to the login page and are no longer logged in
        self.assertRedirects(response, "/login/")
        self.assertFalse(session.get("LoggedIn", False))
        self.assertNotIn("name", session)
        self.assertNotIn("role", session)

class LogoutAcceptance(TestCase):
    client = None

    def setUp(self):
        self.client = Client()
        account = Account(account_id=1, username="Joe", password="12345", role=0, name="Joe Schmo")
        account.save()
    def test_SuccessfulLogout(self):
        login_response = self.client.post('/login/', {'username': 'Joe', 'password': '12345'}, follow = True)
        self.assertRedirects(login_response, '/dashboard/')  # Update with the expected redirect URL

        # Now, test the logout
        logout_response = self.client.get('/logout/')
        self.assertRedirects(logout_response, '/login/')  # Assuming the user is redirected to the login page

        # Check if session data is cleared
        self.assertEqual(self.client.session.get('LoggedIn'), False)
        self.assertEqual(self.client.session.get('name'), None)
        self.assertEqual(self.client.session.get('role'), None)
class CreateAccountAcceptance(TestCase):
    # As a supervisor or administrator, I need to be able to create instructor and TA accounts so that random people can’t get in the system.
    client = None

    def setUp(self):
        self.client = Client()
        self.account = Account.objects.create(
            account_id=1, username="Joe", password="12345", role=0, name="Joe Schmo"
        )
        self.account.save()
        # Log in the client
        self.client.post("/login/", {"username": "Joe", "password": "12345"})

    def test_criteriaOne(self):
        # GIVEN a user already exists with a certain username
        existing_account = self.account
        old_num_accounts = Account.objects.count()

        # And the logged in user has the proper permissions
        response = self.client.get("/manage/createAccount/")
        self.assertEqual(response.status_code, 200)

        # WHEN an admin attempts to create an account with that name
        response = self.client.post(
            "/manage/createAccount/",
            {
                "username": "Joe",
                "name": "Joe",
                "phone": "1234567890",
                "email": "new@example.com",
                "address": "New Address",
                "password": "new_password",
                "acctype": "instructor",
            },
        )
        # THEN no change happens to the database
        self.assertEqual(Account.objects.count(), old_num_accounts)
        self.assertContains(
            response, "There is already an account with that username.", status_code=200
        )

    def test_criteriaTwo(self):
        # GIVEN an account with a certain username doesn’t exist yet

        # WHEN an admin attempts to create that account
        response = self.client.post(
            "/manage/createAccount/",
            {
                "username": "NewUser",
                "name": "NewUser",
                "phone": "1234567890",
                "email": "new@example.com",
                "address": "New Address",
                "password": "new_password",
                "acctype": "instructor",
            },
            follow=True,
        )
        # Check if the request was successful (status code 200 OK)
        self.assertEqual(response.status_code, 200)

        # THEN the account is created in the database with no assigned course or information
        new_account = Account.objects.get(username="NewUser")
        self.assertEqual(new_account.role, 1)

        # AND the account can be logged into from another computer
        response = self.client.post(
            "/login/", {"username": "NewUser", "password": "new_password"}, follow=True
        )

        session = self.client.session
        self.assertEqual(session["name"], "NewUser")
        self.assertEqual(session["role"], 1)
        self.assertTrue(session["LoggedIn"])


class DeleteAccountAcceptance(TestCase):
    # As a supervisor or administrator, I want to be able to delete accounts so that if someone leaves UWM they don’t stay in the system.
    client = None

    def setUp(self):
        self.client = Client()
        self.clientSupervisor = Account.objects.create(
            account_id=1, username="Joe", password="12345", role=0, name="Joe Schmo"
        )
        self.accountToDelete = Account.objects.create(
            account_id=2, username="Bob", password="12345", role=1, name="Bob B."
        )
        self.accountToDelete.save()
        self.clientSupervisor.save()

        # Log in the client
        self.client.post("/login/", {"username": "Joe", "password": "12345"})

    def test_criteriaOne(self):
        # GIVEN the admin is on the page with all accounts
        response = self.client.get("/manage/", follow=True)
        # WHEN they click on an account
        account_id_to_delete = self.accountToDelete.account_id
        # THEN there is an option to delete it
        response = self.client.post(
            "/manage/deleteAccount/", {"userId": account_id_to_delete}, follow=True
        )
        self.assertContains(response, "Account Deleted Successfully")
        # AND the admin is prompted to confirm the deletion if they select that option


class EditAccountAcceptance(TestCase):
    # As a supervisor or administrator, I want to be able to edit the information on other accounts
    # so that if someone enters the wrong information it is quickly corrected.
    client = None

    def setUp(self):
        self.client = Client()
        self.account = Account.objects.create(
            account_id=1, username="Joe", password="12345", role=0, name="Joe Schmo"
        )
        self.clientSupervisor = Account.objects.create(
            account_id=5,
            username="Admin",
            password="admin",
            role=0,
            name="Admin Sadmin",
        )
        # Save the accounts
        self.account.save()
        self.clientSupervisor.save()
        # Log in the client
        self.client.post("/login/", {"username": "Admin", "password": "admin"})

    def test_criteriaOne(self):
        # GIVEN the admin is on the page with all accounts
        response = self.client.get("/manage/", follow=True)
        # WHEN they click on an account
        account_id = self.account.account_id
        # AND click the edit button with an account selected
        response = self.client.get(
            f"/manage/editAccount/?userId={account_id}", follow=True
        )

        # THEN there is an option to edit the account’s information
        self.assertContains(response, "Edit Account")

    def test_criteriaTwo(self):
        # GIVEN the admin has selected an account and navigated to the edit page
        account_id = self.account.account_id
        response = self.client.get(
            f"/manage/editAccount/?userId={account_id}", follow=True
        )

        self.assertEqual(response.status_code, 200)
        # WHEN they enter new info and press the submit button
        response = self.client.post(
            f"/manage/editAccount/?userId={account_id}",
            {
                "username": "Joe",
                "password": "54321",
                "name": "Joe S.",
                "role": "0",
                "phone": "1234567890",
                "email": "joe@example.com",
                "address": "123 Main St",
                "office_hour_location": "Room 101",
                "office_hour_time": "9:00 AM - 11:00 AM",
            },
            follow=True,
        )
        # THEN the account is updated in the database
        updated_account = Account.objects.get(username="Joe")
        self.assertEqual(updated_account.password, "54321")

        # AND the admin sees a confirmation message
        self.assertContains(response, "Account information updated successfully.")

    def test_criteriaThree(self):
        # GIVEN the admin has selected an account and navigated to the edit page
        account_id = self.account.account_id
        A = Account.objects.get(account_id = account_id)
        response = self.client.get(
            f"/manage/editAccount/?userId={account_id}", follow=True
        )

        # WHEN the admin entered the same information the account already has
        response = self.client.post(
            f"/manage/editAccount/?userId={account_id}",
            {
                "username": "Joe",
                "password": "12345",
                "name": "Joe Schmo",
                "role": "0",
                "phone": "1234567890",
                "email": "joe@example.com",
                "address": "123 Main St",
                "office_hour_location": "Room 101",
                "office_hour_time": "9:00 AM - 11:00 AM",
            },
            follow=True,
        )

        # AND they press the submit button
        self.assertEqual(response.status_code, 200)

        # THEN No Changes were made
        self.assertEqual(A.username, "Joe")
        self.assertEqual(A.password, '12345')
        self.assertEqual(A.name, "Joe Schmo")
        self.assertEqual(A.role, 0)
        

    def test_criteriaFour(self):
        # GIVEN the admin has selected an account and navigated to the edit page
        account_id = self.account.account_id
        response = self.client.get(
            f"/manage/editAccount/?userId={account_id}", follow=True
        )

        # WHEN a required field (login details) is blank in the request
        response = self.client.post(
            f"/manage/editAccount/?userId={account_id}",
            {
                "username": "Joe",
                "password": "",
                "name": "Joe Schmo",
                "role": "0",
                "phone": "1234567890",
                "email": "joe@example.com",
                "address": "123 Main St",
                "office_hour_location": "Room 101",
                "office_hour_time": "9:00 AM - 11:00 AM",
            },
            follow=True,
        )

        # AND the admin presses the submit button
        self.assertEqual(response.status_code, 200)

        # THEN the database is not updated
        unchanged_account = Account.objects.get(username="Joe")
        self.assertEqual(unchanged_account.password, "12345")

        # AND they see a message saying that they need to enter information
        self.assertContains(response, "Login fields cannot be empty")
