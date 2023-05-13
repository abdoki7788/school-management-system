# Generated by Django 4.1.4 on 2023-05-13 03:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("attendance", "0007_alter_class_options_alter_student_class_room"),
    ]

    operations = [
        migrations.AddField(
            model_name="student",
            name="discipline",
            field=models.CharField(
                choices=[
                    ("red", "قرمز"),
                    ("green", "سبز"),
                    ("white", "سفید"),
                    ("yellow", "زرد"),
                ],
                default="white",
                max_length=6,
            ),
        ),
    ]
