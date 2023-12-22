import unittest
from django.test import TestCase, RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from CS361_Project.models import *
from CS361_Project.functions import *

class TestManagementUser(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = Account.objects.create(username='testuser', password='testpassword', role=1, name='Test User')

    def test_login(self):
        request = self.factory.get('/')
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()

        Management.User.login(request, self.user)
        self.assertEqual(request.session['userID'], self.user.account_id)
        self.assertEqual(request.session['name'], self.user.name)
        self.assertEqual(request.session['role'], self.user.role)
        self.assertTrue(request.session['LoggedIn'])

    def test_authenticate_user(self):
        user = Management.User.authenticate_user('testuser', 'testpassword')
        self.assertEqual(user, self.user)

        user = Management.User.authenticate_user('wronguser', 'wrongpassword')
        self.assertIsNone(user)

    def test_logout(self):
        request = self.factory.get('/')
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()

        Management.User.login(request, self.user)
        Management.User.logout(request)
        self.assertFalse(request.session['LoggedIn'])

class TestManagementAccount(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = Account.objects.create(username='testuser', password='testpassword', role=1, name='Test User')

    def test_get_from_id(self):
        user = Management.Account.get_from_id(self.user.account_id)
        self.assertEqual(user, self.user)

        user = Management.Account.get_from_id(-1)
        self.assertIsNone(user)

    def test_edit_account_GETview(self):
        request = self.factory.get('/', {'userId': self.user.account_id})
        response = Management.Account.edit_account_GETview(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user'], self.user)

        request = self.factory.get('/', {'userId': -1})
        response = Management.Account.edit_account_GETview(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Account with ID -1 does not exist.', response.content.decode())

class TestManagementCourse(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.course = Course.objects.create(name='testcourse', description='testdescription')
        self.instructor = Account.objects.create(username='testinstructor', password='testpassword', role=2, name='Test Instructor')

    def test_manage_course(self):
        request = self.factory.post('/', {'selected_course_id': self.course.Courseid})
        result = Management.Course.manage_course(request)
        self.assertEqual(result['selected_course'], self.course)

        request = self.factory.post('/', {'selected_course_id': -1})
        result = Management.Course.manage_course(request)
        self.assertIsNone(result['selected_course'])

    def test_create_course(self):
        request = self.factory.post('/', {'name': 'newcourse', 'dept': 'newdepartment', 'professor': self.instructor.account_id})
        Management.Course.create_course(request)
        new_course = Course.objects.get(name='newcourse')
        self.assertIsNotNone(new_course)
        self.assertEqual(new_course.dept, 'newdepartment')
        self.assertEqual(new_course.instructor.instructor_id, self.instructor)

        request = self.factory.post('/', {'name': 'newcourse2', 'dept': 'newdepartment2', 'professor': -1})
        with self.assertRaises(Instructor.DoesNotExist):
            Management.Course.create_course(request)

class TestManagementProfile(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = Account.objects.create(username='testuser', password='testpassword', role=1, name='Test User')

    def test_edit_profile_data(self):
        request = self.factory.post('/', {'name': 'New Name'})
        Management.Profile.edit_profile_data(request, self.user, 'name', str, 'Name')
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, 'New Name')

        request = self.factory.post('/', {'name': 123})
        with self.assertRaises(TypeError):
            Management.Profile.edit_profile_data(request, self.user, 'name', str, 'Name')

        request = self.factory.post('/', {'name': 'Null'})
        with self.assertRaises(ValueError):
            Management.Profile.edit_profile_data(request, self.user, 'name', str, 'Name')

    def test_edit_profile(self):
        request = self.factory.post('/', {'Name': 'New Name', 'Phone': '1234567890', 'Email': 'newemail@test.com', 'Address': 'New Address', 'Location': 'New Location', 'Time': 'New Time'})
        Management.Profile.edit_profile(request, self.user)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, 'New Name')
        self.assertEqual(self.user.phone, '1234567890')
        self.assertEqual(self.user.email, 'newemail@test.com')
        self.assertEqual(self.user.address, 'New Address')
        self.assertEqual(self.user.office_hour_location, 'New Location')
        self.assertEqual(self.user.office_hour_time, 'New Time')