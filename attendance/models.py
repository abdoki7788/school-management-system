from django.db import models
from django.utils import timezone
import os
from datetime import datetime
from accounts.models import User
from . import validators

# Create your models here.

def student_image_upload(instance, filename):
    now = timezone.now()
    base, extension = os.path.splitext(filename.lower())
    return f"students/{instance.full_name()}/{now:%Y-%m-%d-%H%M%S}{extension}"

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
    image = models.ImageField(default='defaults/person.png', upload_to=student_image_upload)
    number = models.CharField(max_length=11, verbose_name="Phone Number")
    student_id = models.CharField(max_length=10, validators=[validators.student_id_validator])
    serial_code = models.CharField(max_length=6, validators=[validators.serial_code_validator])
    class_room = models.ForeignKey("Class", verbose_name="Class", on_delete=models.SET_NULL, null=True, related_name="students")
    
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
    def __str__(self):
        return self.full_name()

class Lesson(models.Model):
    lesson_name = models.CharField(max_length=50)
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='teached_lessons')
    
    def __str__(self) -> str:
        return f"{self.lesson_name} توسط {self.teacher}"

    class Meta:
        unique_together = ['lesson_name', 'teacher']


class WeeklySchedule(models.Model):
    satureday = models.ManyToManyField(Lesson, related_name='satureday')
    sunday = models.ManyToManyField(Lesson, related_name='sunday')
    monday = models.ManyToManyField(Lesson, related_name='monday')
    tuesday = models.ManyToManyField(Lesson, related_name='tuesday')
    wednesday = models.ManyToManyField(Lesson, related_name='wednesday')

    def __str__(self) -> str:
        return f"برنامه هفتگی کلاس {self.class_room}"

class Class(models.Model):
    class_id = models.CharField(max_length=3, primary_key=True)
    weekly_schedule = models.OneToOneField(WeeklySchedule, on_delete=models.SET_NULL, null=True, blank=True, related_name='class_room')

    def students_count(self):
        return self.students.count()
    
    def __str__(self) -> str:
        return self.class_id