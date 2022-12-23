# Generated by Django 4.1.4 on 2022-12-08 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="type",
            field=models.CharField(
                choices=[("H", "Headmaster"), ("S", "Staff"), ("T", "Teacher")],
                max_length=1,
            ),
        ),
    ]