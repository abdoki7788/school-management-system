# Generated by Django 4.1.4 on 2023-03-17 17:42

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("attendance", "0001_initial"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="lesson",
            unique_together={("lesson_name", "teacher")},
        ),
    ]
