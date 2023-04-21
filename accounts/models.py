from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


# Create your models here.

@deconstructible
class UnicodeUsernameValidator(validators.RegexValidator):
    regex = r"^[\w.@\+\-\s]+\Z"
    message = _(
        "Enter a valid username. This value may contain only letters, "
        "numbers, and @/./+/-/_ characters and spaces."
    )
    flags = 0


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