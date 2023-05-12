# Generated by Django 4.1.4 on 2023-05-12 10:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("attendance", "0006_lesson_priority"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="class",
            options={"ordering": ["-class_id"]},
        ),
        migrations.AlterField(
            model_name="student",
            name="class_room",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="students",
                to="attendance.class",
                verbose_name="Class",
            ),
        ),
    ]
