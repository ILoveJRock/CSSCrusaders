from django.test import TestCase

from CS361_Project.models import User

class UserAcceptanceTest(TestCase):
    def test_create_user(self):
        # Create a new user
        username = 'testuser'
        email = 'testuser@example.com'
        password = 'testpassword'
        role = 1  # Assuming 1 represents the 'Student' role

        user = User(username=username, email=email, password=password, role=role)
        user.save()

        # Retrieve the user from the database
        created_user = User.objects.get(username=username)

        # Verify that the created user has the correct details
        self.assertEqual(created_user.username, username)
        self.assertEqual(created_user.email, email)
        self.assertEqual(created_user.role, role)

    def test_update_user(self):
        # Create a new user
        username = 'testuser'
        email = 'testuser@example.com'
        password = 'testpassword'
        role = 1  # Assuming 1 represents the 'Student' role

        user = User(username=username, email=email, password=password, role=role)
        user.save()

        # Retrieve the user from the database
        existing_user = User.objects.get(username=username)

        # Update the user's email and save the changes
        new_email = 'updated_email@example.com'
        existing_user.email = new_email
        existing_user.save()

        # Retrieve the user again from the database
        updated_user = User.objects.get(username=username)

        # Verify that the updated user has the new email
        self.assertEqual(updated_user.email, new_email)