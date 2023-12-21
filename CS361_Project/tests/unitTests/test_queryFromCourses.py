from django.test import TestCase
from CS361_Project.functions import queryFromCourses
from CS361_Project.models import Course

class TestConvert(TestCase):
    mock_courses = None
    mock_labs = None
    mock_junctions = None

    def setUp(self):
        self.mock_courses = [
            {
                "name": "Intro to software engineering",
                "dept": "Compsci",
                "id": 1
            },
            {
                "name": "DS&A",
                "dept": "Compsci",
                "id": 2
            }
        ]

        self.mock_instructors = [
            {
                "id": 1,
                "course": 1
            },
            {
                "id": 3,
                "course": 2
            }
        ]

        self.mock_accounts = [
            {
                "id": 1,
                "name": "joe shmo"
            },
            {
                "id": 2,
                "name": "not instructor"
            },
            {
                "id": 3,
                "name": "prof trelawney"
            }
        ]

    def test_retain_courses(self):
        query = queryFromCourses(self.mock_courses, self.mock_instructors, self.mock_accounts)
        for i in range(self.mock_courses):
            for key in self.mock_courses[i].keys():
                self.assertTrue(self.mock_courses[i][key] == query[i][key], "not every course was transferred to query")

    def test_no_extra_accounts(self):
        query = queryFromCourses(self.mock_courses, self.mock_instructors, self.mock_accounts)
        for course in query:
            self.assertFalse(course["instructor"] == "not instructor", "non-instructor was set as instructor")
