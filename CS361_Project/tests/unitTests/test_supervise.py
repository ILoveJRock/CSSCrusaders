from django.test import TestCase

from CS361_Project.models import Course, Section, User, Role

from classes.course_class import CourseClass
from classes.section_class import SectionClass
from classes.user_class import UserClass
from classes.supervisor_class import SupervisorClass
from classes.instructor_class import InstructorClass
from classes.ta_class import TAClass


class SupervisorUnitTestSuite(TestCase):
    def setUp(self):
        self.supervisor_class = SupervisorClass('supervisor', 'supervisor@uwm.edu', 'Test', 'Supervisor')
        self.supervisor_class.save_details()

        self.instructor = InstructorClass('instructor', 'instructor@uwm.edu', 'Test', 'Instructor')
        self.instructor.save_details()
        self.instructor = self.instructor.get_model_instance()

        self.ta = TAClass('ta', 'ta@uwm.edu', 'Test', 'TA')
        self.ta.save_details()
        self.ta = self.ta.get_model_instance()

        self.course = CourseClass(subject='COMPSCI', number='361', name='Intro to Software Engineering')
        self.course.save_details()
        self.course = self.course.get_model_instance()

        self.section = SectionClass('891', self.course)
        self.section.save_details()
        self.section = self.section.get_model_instance()

    def test_init_default(self):
        supervisor_class = SupervisorClass('supervisor', 'supervisor@uwm.edu', 'Test', 'Supervisor',
                                           phone_number='1111111111', home_address='123 Main St.')

        self.assertEqual(supervisor_class.username, 'supervisor')
        self.assertEqual(supervisor_class.email, 'supervisor@uwm.edu')
        self.assertEqual(supervisor_class.first_name, 'Test')
        self.assertEqual(supervisor_class.last_name, 'Supervisor')
        self.assertEqual(supervisor_class.phone_number, '1111111111')
        self.assertEqual(supervisor_class.home_address, '123 Main St.')
        self.assertEqual(supervisor_class.courses, [])
        self.assertEqual(supervisor_class.sent_notifications, [])
        self.assertEqual(supervisor_class.received_notifications, [])

    def test_get_instance_default(self):
        supervisor_class = SupervisorClass.get_instance(self.supervisor_class.get_model_instance())

        self.assertTrue(isinstance(supervisor_class, SupervisorClass))

        self.assertEqual(supervisor_class.username, self.supervisor_class.username)
        self.assertEqual(supervisor_class.email, self.supervisor_class.email)
        self.assertEqual(supervisor_class.first_name, self.supervisor_class.first_name)
        self.assertEqual(supervisor_class.last_name, self.supervisor_class.last_name)
        self.assertEqual(supervisor_class.role, self.supervisor_class.role)
        self.assertEqual(supervisor_class.courses, self.supervisor_class.courses)
        self.assertEqual(supervisor_class.sent_notifications, self.supervisor_class.sent_notifications)
        self.assertEqual(supervisor_class.received_notifications, self.supervisor_class.received_notifications)

    def test_get_courses(self):
        self.assertEqual(list(self.supervisor_class.get_courses()), [self.course])

    def test_has_course_default(self):
        courses = Course.objects.all()

        for course in courses:
            self.assertTrue(self.supervisor_class.has_course(course))

    def test_has_course_true(self):
        self.assertEqual(self.supervisor_class.has_course(self.course), True)

    def test_has_course_false(self):
        invalid_course = Course(subject='ELECENG', number='330', name='Electronics 1')
        self.assertFalse(self.supervisor_class.has_course(invalid_course))

    def test_get_sections(self):
        all_sections = self.supervisor_class.get_sections()
        self.assertEqual(list(all_sections), [self.section])

    def test_has_section_true(self):
        self.assertTrue(self.supervisor_class.has_section(self.section))

    def test_has_section_false(self):
        invalid_section = SectionClass('801', self.course)
        self.assertFalse(self.supervisor_class.has_section(invalid_section))

    def test_create_user_default(self):
        user = self.supervisor_class.create_user('test', 'test@uwm.edu', 'foobar123', 'Test', 'User')

        self.assertTrue(user.check_password('foobar123'))

        self.assertEqual(user.username, 'test')
        self.assertEqual(user.email, 'test@uwm.edu')
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'User')
        self.assertEqual(user.role, Role.TA)
        self.assertEqual(user.phone_number, None)
        self.assertEqual(user.home_address, None)
        self.assertEqual(list(user.courses.all()), [])
        self.assertEqual(list(user.sent_notifications.all()), [])
        self.assertEqual(list(user.received_notifications.all()), [])

    def test_delete_user_default(self):
        user = UserClass('test', 'test@uwm.edu', 'Test', 'User')
        user.save_details()
        user = user.get_model_instance()

        self.supervisor_class.delete_user(user)

        with self.assertRaises(User.DoesNotExist, msg='delete_user fails to delete the user from the db'):
            user_class = UserClass.get_instance(user)
            user_class.get_model_instance()
    
    def test_delete_user_does_not_exist(self):
        invalid_user = UserClass('invalid', 'invalid@uwm.edu', 'Invalid', 'User')

        with self.assertRaises(AttributeError, msg='delete_user does not raise AttributeError for non-existant user'):
            self.supervisor_class.delete_user(invalid_user)

    def test_edit_user_default(self):
        self.ta = self.supervisor_class.edit_user(self.ta, 'test', 'test@uwm.edu', 'foobar123', 'Test', 'User', Role.SUPERVISOR)

        self.assertTrue(self.ta.check_password('foobar123'))

        self.assertEqual(self.ta.username, 'test')
        self.assertEqual(self.ta.email, 'test@uwm.edu')
        self.assertEqual(self.ta.first_name, 'Test')
        self.assertEqual(self.ta.last_name, 'User')
        self.assertEqual(self.ta.role, Role.SUPERVISOR)
        self.assertEqual(self.ta.phone_number, None)
        self.assertEqual(self.ta.home_address, None)

    def test_create_course_default(self):
        course = self.supervisor_class.create_course('COMPSCI', '337', 'Systems Programming', self.instructor)
        
        self.assertEqual(course.subject, 'COMPSCI')
        self.assertEqual(course.number, '337')
        self.assertEqual(course.name, 'Systems Programming')
        self.assertEqual(course.instructor, self.instructor)

    def test_delete_course_default(self):
        course = CourseClass('COMPSCI', '337', 'Systems Programming', self.instructor)
        course.save_details()
        course = course.get_model_instance()

        self.supervisor_class.delete_course(course)

        with self.assertRaises(Course.DoesNotExist, msg='delete_course fails to delete the course from the db'):
            course_class = CourseClass.get_instance(course)
            course_class.get_model_instance()

    def test_delete_course_does_not_exist(self):
        invalid = CourseClass('INVALID', '0', 'Invalid')

        with self.assertRaises(Course.DoesNotExist, msg='delete_course does not raise Course.DoesNotExist for non-existant course'):
            self.supervisor_class.delete_course(invalid)

    def test_edit_course_default(self):
        self.course = self.supervisor_class.edit_course(self.course, 'COMPSCI', '337', 'Systems Programming')

        self.assertEqual(self.course.subject, 'COMPSCI')
        self.assertEqual(self.course.number, '337')
        self.assertEqual(self.course.name, 'Systems Programming')
        self.assertEqual(self.course.instructor, None)
    
    def test_create_section_default(self):
        section = self.supervisor_class.create_section(self.course, '892')
        course_class = CourseClass.get_instance(self.course)

        self.assertEqual(section.number, '892')
        self.assertEqual(section.course, self.course)
        self.assertIn(section, course_class.get_sections())

    def test_delete_section_default(self):
        section = SectionClass('892', self.course)
        section.save_details()
        section = section.get_model_instance()

        self.supervisor_class.delete_section(section)

        with self.assertRaises(Section.DoesNotExist, msg='Failed to delete section from the db'):
            section_class = SectionClass.get_instance(section)
            section_class.get_model_instance()

    def test_delete_section_does_not_exist(self):
        invalid = SectionClass('0', None)

        with self.assertRaises(AttributeError, msg='delete_section does not raise AttributeError for non-existant section'):
            self.supervisor_class.delete_course(invalid)

    def test_assign_instructor_course_default(self):
        self.supervisor_class.assign_instructor_course(self.instructor, self.course)

        self.assertEqual(self.course.instructor, self.instructor)
        self.assertIn(self.course, self.instructor.courses.all())

    def test_assign_instructor_course_instructor_does_not_exist(self):
        invalid = InstructorClass('invalid', 'invalid@uwm.edu', 'Invalid', 'Instructor')

        with self.assertRaises(AttributeError, msg='assign_instructor_course does not raise AttributeError for non-existant instructor'):
            self.supervisor_class.assign_instructor_course(invalid, self.course)

    def test_assign_instructor_course_course_does_not_exist(self):
        invalid = CourseClass('INVALID', '0', 'Invalid')

        with self.assertRaises(TypeError, msg='assign_instructor_course does not raise TypeError for non-existant course'):
            self.supervisor_class.assign_instructor_course(self.instructor, invalid)

    def test_assign_ta_course_default(self):
        self.supervisor_class.assign_ta_course(self.ta, self.course)

        self.assertIn(self.course, self.ta.courses.all())
        self.assertIn(self.ta, self.course.user_set.all())

    def test_assign_ta_course_ta_does_not_exist(self):
        invalid = TAClass('invalid', 'invalid@uwm.edu', 'Invalid', 'TA')

        with self.assertRaises(AttributeError, msg='assign_ta_course does not raise AttributeError for non-existant TA'):
            self.supervisor_class.assign_ta_course(invalid, self.course)

    def test_assign_ta_course_course_does_not_exist(self):
        invalid = CourseClass('INVALID', '0', 'Invalid')

        with self.assertRaises(TypeError, msg='assign_ta_course does not raise TypeError for non-existant course'):
            self.supervisor_class.assign_ta_course(self.ta, invalid)

    def test_send_notifications(self):
        notifications = self.supervisor_class.send_notifications('Subject', 'Message')

        supervisor = self.supervisor_class.get_model_instance()

        for notification in notifications:
            self.assertIn(notification, supervisor.sent_notifications.all())
            self.assertNotIn(notification, supervisor.received_notifications.all())

            self.assertNotIn(notification, notification.recipient.sent_notifications.all())
            self.assertIn(notification, notification.recipient.received_notifications.all())