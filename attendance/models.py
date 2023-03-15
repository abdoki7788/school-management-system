from django.db import models
from datetime import datetime
from accounts.models import User

# Create your models here.

class Attendance(models.Model):
    class_room = models.ForeignKey("Class", on_delete=models.CASCADE, related_name="attendances")
    absents = models.ManyToManyField("Student", related_name="absent", blank=True)
    presents = models.ManyToManyField("Student", related_name="present", blank=True)
    date = models.DateField(default=datetime.now)

    def detail(self):
        return self
    class Meta:
        unique_together = ['class_room', 'date']

class Student(models.Model):
    first_name = models.CharField(verbose_name="First Name", max_length=50)
    last_name = models.CharField(verbose_name="Last Name", max_length=50)
    number = models.CharField(max_length=11, verbose_name="Phone Number")
    class_room = models.ForeignKey("Class", verbose_name="Class", on_delete=models.SET_NULL, null=True, related_name="students")


class Class(models.Model):
    class_id = models.CharField(max_length=3)

    def students_count(self):
        return self.students.count()