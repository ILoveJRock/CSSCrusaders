from django.forms import ValidationError

# from project_app.models import Course, User, Role


# class CourseClass:
#     def __init__(self, subject, number, name='', instructor=None):
#         self.subject = subject
#         self.number = number
#         self.name = name
#         self.instructor = instructor

#     @classmethod
#     def get_instance(cls, course):
#         return cls(course.subject, course.number, course.name, course.instructor)

#     def save_details(self):
#         course = Course(name=self.name, subject=self.subject,
#                         number=self.number, instructor=self.instructor)
#         course.save()
#         return f'Added {self.subject} {self.number} to the system.'

#     def get_model_instance(self):
#         return Course.objects.get(subject=self.subject, number=self.number)

#     def validate(self):
#         pass

#     def delete(self):
#         course = self.get_model_instance()
#         course.delete()

#     def get_subject(self):
#         return self.subject

#     def set_subject(self, subject):
#         course = self.get_model_instance()
#         course.subject = subject
#         course.save()

#         self.subject = subject

#     def get_number(self):
#         return self.number

#     def set_number(self, number):
#         course = self.get_model_instance()
#         course.number = number
#         course.save()

#         self.number = number

#     def get_name(self):
#         return self.name

#     def set_name(self, name):
#         course = self.get_model_instance()
#         course.name = name
#         course.save()

#         self.name = name

#     def get_instructor(self):
#         return self.instructor

#     def set_instructor(self, instructor):
#         course = self.get_model_instance()
#         course.instructor = instructor
#         course.save()

#         self.instructor = instructor

#     def get_tas(self):
#         course = self.get_model_instance()
#         return course.user_set.filter(role=Role.TA)

#     def get_sections(self):
#         course = self.get_model_instance()
#         return course.section_set.all()
    