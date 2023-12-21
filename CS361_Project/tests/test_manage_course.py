#from django.test import TestCase, Client

from CS361_Project.models import Course
#Commented because it isn't done
# class EditAccountTests(TestCase):
class EditAccountTests():
    client = None

    def setUp(self):
        self.client = Client()
        self.course = Course(
            name="CS361",
            dept="Computer science"
        )
        self.course.save()

    def test_changesMade(self):
        # Test if changes are successfully made to the course
        updated_data = {
            "name": "Matrices & applications",
            "dept": "MATH"
        }

        # Ensure the account exists with the initial data
        self.assertEqual(self.course.name, 'CS361')

        # When a new post request with updated data is submitted...
        response = self.client.post(f'/course/editCourse/?Labid={self.course.Labid}', {'userId': self.course.Labid, **updated_data})
        # The account information should change accordingly
        updated_course = Course.objects.get(Labid=self.course.Labid)
        # Assert that the account information has been updated to match updated_data
        self.assertEqual(updated_course.name, updated_data['name'])
        self.assertEqual(updated_course.dept, updated_data['dept'])

        # After changes are made, the user should be redirected to the ManageAccount view
        self.assertRedirects(response, '/course/')


    def test_emptyLogin(self):
        bad_data = {
            'username': '',  # Empty username should be invalid
            'password': '',  # Empty password should be invalid
        }
        # When a new post request with bad data is submitted...
        response = self.client.post(f'/manage/editAccount/?userId={self.account.account_id}',
                                    {'userId': self.account.account_id, **bad_data})
        # The form is re-rendered with errors
        self.assertContains(response, 'Login fields cannot be empty')  # Check for a required field error

    def test_nameTaken(self):
        # Test if the form submission fails when trying to change to an existing course name
        existing_name = 'CS361'
        existing_course = Course.objects.create(
            name=existing_name,
            dept="not Computer science"
        )
        existing_course.save()

        new_data = {
            'name' : existing_name,
            "dept": "Computer science"
        }

        # When a new post request with a taken name is submitted...
        response = self.client.post(f'/course/editCourse/?Labid={self.course.Labid}',
                                    {'Labid': self.course.Labid, **new_data})

        # Check if the form is re-rendered with a name taken error
        self.assertContains(response, 'A course with that name already exists.')

    def test_nonexistentUser(self):
        # Test if the view handles a request for a nonexistent user ID
        invalid_Labid = 999999999 # assuming this is not in the database

        with self.assertRaises(Course.DoesNotExist):
            # Send a POST request to the editAccount view with an invalid user ID
            # Follow the redirects to handle any redirects (e.g., to an error page)
            self.client.post(
                f'/manage/editAccount/?userId={self.course.Labid}',
                {'userId': invalid_Labid},
                follow=True
            )