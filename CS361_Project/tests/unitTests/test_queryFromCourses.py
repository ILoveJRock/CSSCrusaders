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
                "dept": "Compsci",
                "id": 1
            },
            {
                "name": "007",
                "dept": "Compsci",
                "id": 2
            },
            {
                "name": "001",
                "dept": "Compsci",
                "id": 3
            }
        ]

        self.mock_junctions = [
            {
                "course": 1,
                "labSection": 2
            },
            {
                "course": 1,
                "labSection": 3
            },
            {
                "course": 2,
                "labSection": 3
            }
        ]

    def test_retain_courses(self):
        query = queryFromCourses(self.mock_courses, self.mock_labs, self.mock_junctions)
        for i in range(self.mock_courses):
            for key in self.mock_courses[i].keys():
                self.assertTrue(self.mock_courses[i][key] == query[i][key], "not every course was transferred to query")

    def test_convert_labs(self):
        query = queryFromCourses(self.mock_courses, self.mock_labs, self.mock_junctions)
        for row in self.mock_junctions:
            course = next(filter(lambda c : c["id"] == row["course"], self.mock_courses))
            lab = next(filter(lambda l : l["id"] == row["labSection"], self.mock_labs))
            query_course = next(filter(lambda c : c["id"] == course["id"]), query)
            self.assertTrue(lab.name in query_course["labs"], "not every lab was in query")
