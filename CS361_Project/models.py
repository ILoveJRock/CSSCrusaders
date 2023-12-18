from django.db import models


class Account(models.Model):
    account_id = models.AutoField(primary_key=True, unique=True)
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=30)
    role = models.IntegerField(choices=[(0, "Supervisor"), (1, "Instructor"), (2, "TA")])
    name = models.CharField(max_length=30, null=True)
    phone = models.CharField(max_length=15, null=True)
    email = models.EmailField(max_length=254, null=True)
    address = models.CharField(max_length=255, null=True)
    office_hour_location = models.CharField(max_length=255, null=True)
    office_hour_time = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.username

class Supervisor(models.Model):
    supervisor_id = models.OneToOneField("Account", on_delete=models.CASCADE, primary_key=True)


class Instructor(models.Model):
    instructor_id = models.OneToOneField("Account", on_delete=models.CASCADE, primary_key=True)
    course = models.ForeignKey("Course", on_delete=models.SET_NULL, null=True)

class TA(models.Model):
    ta_id = models.OneToOneField("Account", on_delete=models.CASCADE, primary_key=True)
    course = models.ForeignKey("Course", on_delete=models.SET_NULL, null=True)

class LabSection(models.Model):
    Labid = models.IntegerField(primary_key=True)
    course = models.ForeignKey("Course", on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=40)

class Course(models.Model):
    Labid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=40, unique=True)
    dept = models.CharField(max_length=40)
