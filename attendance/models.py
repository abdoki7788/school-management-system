from django.db import models
from django.utils import timezone

import os
from datetime import datetime

from accounts.models import User
from . import validators

# My Database Models


## student image upload path generator function
def student_image_upload(instance, filename):
    now = timezone.now()
    base, extension = os.path.splitext(filename.lower())
    return f"students/{instance.full_name()}/{now:%Y-%m-%d-%H%M%S}{extension}"


##  attendances model (not needed yet)
class Attendance(models.Model):
    class_room = models.ForeignKey("Class", on_delete=models.CASCADE, related_name="attendances")
    absents = models.ManyToManyField("Student", related_name="absent", blank=True)
    presents = models.ManyToManyField("Student", related_name="present", blank=True)
    date = models.DateField(default=datetime.now)

    def detail(self):
        return self
    class Meta:
        unique_together = ['class_room', 'date']

## student model
class Student(models.Model):
    DISCIPLINE_CHOICES = (
        ("red", "red"),
        ("green", "green"),
        ("white", "white"),
        ("yellow", "yellow"),
    )

    first_name = models.CharField("نام", max_length=50)
    last_name = models.CharField("نام خانوادگی", max_length=50)
    image = models.ImageField("عکس", default='defaults/person.png', upload_to=student_image_upload, blank=True)
    number = models.CharField("شماره تلفن", max_length=11)
    student_id = models.CharField("شماره شناسنامه", max_length=10, validators=[validators.student_id_validator])
    serial_code = models.CharField("کد سریال شناسنامه", max_length=6, validators=[validators.serial_code_validator])
    class_room = models.ForeignKey("Class", verbose_name="کلاس", on_delete=models.SET_NULL, null=True, blank=True, related_name="students")
    discipline = models.CharField("سطح انظباط", max_length=6, choices=DISCIPLINE_CHOICES, default="white")
    
    class Meta:
        verbose_name = "دانش آموز"
        verbose_name_plural = "دانش آموز ها"

    # get student full name by binding first_name and last_name
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def save(self, *args, **kwargs):
        ## it will do extra validations
        self.full_clean()
        return super().save(*args, **kwargs)
    def __str__(self):
        return self.full_name()

class Lesson(models.Model):
    lesson_name = models.CharField(max_length=50)
    teacher = models.CharField(max_length=50, null=True)
    ## lesson time priority
    priority = models.IntegerField(default=1)
    
    def __str__(self) -> str:
        return f"{self.lesson_name} توسط {self.teacher}"

    class Meta:
        # lessons should be unique by lesson_name and teacher . that means 
        # lessons with same lesson_name and teacher cant be created
        unique_together = ['lesson_name', 'teacher']


## classes weekly schedule
class WeeklySchedule(models.Model):
    satureday = models.ManyToManyField(Lesson, related_name='satureday')
    sunday = models.ManyToManyField(Lesson, related_name='sunday')
    monday = models.ManyToManyField(Lesson, related_name='monday')
    tuesday = models.ManyToManyField(Lesson, related_name='tuesday')
    wednesday = models.ManyToManyField(Lesson, related_name='wednesday')


class Class(models.Model):
    class_id = models.CharField(max_length=3, primary_key=True)
    weekly_schedule = models.OneToOneField(WeeklySchedule, on_delete=models.SET_NULL, null=True, blank=True, related_name='class_room')

    class Meta:
        ordering = ['-class_id']
        verbose_name = "کلاس"
        verbose_name_plural = "کلاس ها"

    # this function returns count of class students
    def students_count(self):
        return self.students.count()
    
    def __str__(self) -> str:
        return self.class_id