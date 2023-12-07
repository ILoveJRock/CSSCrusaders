from unittest.mock import MagicMock

from django.test import TestCase, Client

from CS361_Project.models import Account


class TestCreateCourse(TestCase):
    def setUp(self):
        pass
    def test_new_course(self):
        pass
    def test_dupl_course(self):
        pass

class TestEditCourse(TestCase):
    def setUp(self):
        pass
    def test_edit_course(self):
        pass
    def test_emptyPostData(self):
        pass
    def test_invalidPostData(self):
        pass
class TestDeleteCourse(TestCase):
    def test_delete_course(self):
        pass
    def test_delete_nonexistant_course(self):
        pass
        