from django.db import models
from django.apps import apps
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser
from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


# Create your models here.

@deconstructible
class UsernameValidator(validators.RegexValidator):
    regex = r"^[\w.@\+\-]+\Z"
    message = _(
        "Enter a valid username. This value may contain only letters, "
        "numbers, and @/./+/-/_ characters and spaces."
    )
    flags = 0


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, identity, password, **extra_fields):
        if not identity:
            raise ValueError("The given identity must be set")
        
        User = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        user = self.model(identity=identity, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, identity, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        return self.create_user(identity, password, **extra_fields)



class User(AbstractBaseUser):
    username_validator = UsernameValidator()
    TYPE_CHOICES = [
        ("H", "مدیر"),
        ("S", "معاون"),
        ("T", "معلم"),
    ]

    identity = models.CharField(
        max_length=60,
        unique=True,
        help_text= "لازم است. ۱۵۰ حرف یا کمتر. فقط حروف, اعداد و @/./+/-/_",
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
        primary_key=True,
        verbose_name="شناسه"
    )
    type = models.CharField(choices=TYPE_CHOICES, max_length=1, verbose_name="نوع کاربر")
    full_name = models.CharField(max_length=60, null=True, blank=True, verbose_name="نام کامل")
    is_staff = models.BooleanField(default=False)


    objects = UserManager()
    USERNAME_FIELD = "identity"

    def has_module_perms(self, module):
        return self.is_staff
    
    def has_perm(self, p):
        return self.is_staff

    def get_display_name(self):
        if self.full_name:
            return self.full_name
        else:
            return self.identity
    
    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"