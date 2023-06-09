# Generated by Django 4.1 on 2023-03-11 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app_all_in_one", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserConfirmation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("email", models.EmailField(default=None, max_length=254)),
                ("code_confirmation", models.TextField(max_length=8)),
            ],
        ),
    ]
