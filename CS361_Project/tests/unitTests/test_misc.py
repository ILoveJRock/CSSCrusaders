import unittest
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from CS361_Project.models import LabSection, TA, Course, Course_LabSection
from CS361_Project.functions import create_lab, update_user_field, update_user_password

class TestFunctions(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.ta = TA.objects.create(ta_id=self.user.id, section_id=None)
        self.course = Course.objects.create(name='testcourse', description='testdescription')

    def test_create_lab(self):
        request = self.factory.post('/', {'name': 'newlab', 'time': '10:00', 'ta': self.ta.ta_id})
        request.session = {'course': self.course.course_id}
        create_lab(request)
        new_lab = LabSection.objects.get(name='newlab')
        self.assertIsNotNone(new_lab)
        self.assertEqual(new_lab.time, '10:00')
        self.assertEqual(new_lab.ta, self.ta.ta_id)

    def test_update_user_field(self):
        update_user_field(self.user, 'username', 'New Name')
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'New Name')

        with self.assertRaises(TypeError):
            update_user_field(self.user, 'username', 123)

        with self.assertRaises(ValueError):
            update_user_field(self.user, 'username', 'Null')

    def test_update_user_password(self):
        with self.assertRaises(ValueError):
            update_user_password(self.user, 'testpassword', 'testpassword')

        with self.assertRaises(TypeError):
            update_user_password(self.user, 123, 123)

        with self.assertRaises(ValueError):
            update_user_password(self.user, 'Null', 'Null')

        with self.assertRaises(ValueError):
            update_user_password(self.user, 'newpassword', 'wrongpassword')

        update_user_password(self.user, 'newpassword', 'newpassword')
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpassword'))

if __name__ == '__main__':
    unittest.main()