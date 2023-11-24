from django.db import models


class Account(models.Model):
    account_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=30)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=254)
    address = models.CharField(max_length=255)
    office_hour_location = models.CharField(max_length=255)
    office_hour_time = models.CharField(max_length=50)
    role = models.IntegerField(choices=[(0, "Supervisor"), (1, "Instructor"), (2, "TA")])

    def __str__(self):
        return self.username


class Supervisor(models.Model):
    supervisor_id = models.OneToOneField(Account, on_delete=models.CASCADE, primary_key=True)
    # TODO Supervisor database


class Instructor(models.Model):
    instructor_id = models.OneToOneField(Account, on_delete=models.CASCADE, primary_key=True)
    # TODO Store course and lab section assigned to instructors


class TA(models.Model):
    ta_id = models.OneToOneField(Account, on_delete=models.CASCADE, primary_key=True)
    # TODO Store course and lab section assigned to TA


class LabSection(models.Model):
    Labid = models.IntegerField(primary_key=True)
    # TODO Store name and department of lab


class Course(models.Model):
    Labid = models.IntegerField(primary_key=True)
    # TODO Store name and department of course


class Course_LabSection(models.Model):
    course = models.ForeignKey("Course", on_delete=models.CASCADE)
    labSection = models.ForeignKey("LabSection", on_delete=models.CASCADE)
