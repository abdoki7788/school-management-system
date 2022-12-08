from django.db import models

# Create your models here.


from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    TYPE_CHOICES = (
        ("H", "Headmaster"),
        ("S", "Staff"),
        ("T", "Teacher"),
    )
    type = models.CharField(choices=TYPE_CHOICES, max_length=1)