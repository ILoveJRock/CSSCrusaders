from django.db import models


class Account(models.Model):
    username = models.CharField(max_length=30, unique = True, primary_key= True)
    password = models.CharField(max_length = 30)
    #TODO Store role and basic info about the user

class Supervisor(models.Model):
    Supervisorid = models.IntegerField(primary_key = True)
    #TODO Supervisor database

class Instructor(models.Model):
    Instructorid = models.IntegerField(primary_key = True)
    #TODO Store course and lab section assigned to instructors

class TA(models.Model):
    TAid = models.IntegerField(primary_key = True)
    #TODO Store course and lab section assigned to TA

class LabSection(models.Model):
    Labid = models.IntegerField(primary_key = True)
    #TODO Store name and department of lab

class Course(models.Model):
    Labid = models.IntegerField(primary_key = True)
    #TODO Store name and department of course

class Course_LabSection(models.Model):
    course = models.ForeignKey("Course",on_delete=models.CASCADE)
    labSection = models.ForeignKey("LabSection", on_delete=models.CASCADE)