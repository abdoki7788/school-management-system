from django.contrib import admin
from .models import Student, Class, Attendance, Lesson, WeeklySchedule

# Register your models here.

admin.site.register(Student)
admin.site.register(Class)
admin.site.register(Attendance)
admin.site.register(Lesson)
admin.site.register(WeeklySchedule)