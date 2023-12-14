from django.test import TestCase
from functions import queryFromCourses
from CS361_Project.models import Course
from functions import queryFromCourses

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

        self.mock_labs = [
            {
                "name": "001",
                "course_id": 1
            },
            {
                "name": "007",
                "course_id": 1
            },
            {
                "name": "001",
                "course_id": 2
            }
        ]

    def test_retain_courses(self):
        query = queryFromCourses(self.mock_courses, self.mock_labs)
        for i in range(self.mock_courses):
            for key in self.mock_courses[i].keys():
                self.assertTrue(self.mock_courses[i][key] == query[i][key], "not every course was transferred to query")

    def test_convert_labs(self):
        query = queryFromCourses(self.mock_courses, self.mock_labs)
        for lab in self.mock_labs:
            course = filter(lambda c : c["id"] == lab["course_id"], self.mock_courses)[0]
            self.assertEqual(course["id"], lab["course_id"], "A lab is not with the right course")
