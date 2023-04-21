from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator

# Create your models here.

class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()
    TYPE_CHOICES = (
        ("H", "Headmaster"),
        ("S", "Staff"),
        ("T", "Teacher"),
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        help_text= "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
        validators=[username_validator],
        error_messages={
            "unique": "A user with that username already exists.",
        },
        primary_key=True
    )
    type = models.CharField(choices=TYPE_CHOICES, max_length=1, default='H')