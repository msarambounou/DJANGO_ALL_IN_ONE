# Generated by Django 4.1 on 2023-03-17 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app_all_in_one", "0005_entreprise_secteur"),
    ]

    operations = [
        migrations.AddField(
            model_name="business_card_social_media",
            name="indicateur",
            field=models.CharField(default=None, max_length=10),
        ),
        migrations.AddField(
            model_name="entreprise_social_media",
            name="indicateur",
            field=models.CharField(default=None, max_length=10),
        ),
    ]
