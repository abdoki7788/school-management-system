# Generated by Django 4.1.4 on 2023-04-11 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("attendance", "0002_alter_lesson_unique_together"),
    ]

    operations = [
        migrations.AddField(
            model_name="student",
            name="serial_code",
            field=models.CharField(default=667890, max_length=6),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="student",
            name="student_id",
            field=models.CharField(default=2038909876, max_length=10),
            preserve_default=False,
        ),
    ]
