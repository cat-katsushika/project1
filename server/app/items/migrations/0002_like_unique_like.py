# Generated by Django 4.2.3 on 2023-09-29 12:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("items", "0001_initial"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="like",
            constraint=models.UniqueConstraint(fields=("item", "user"), name="unique_like"),
        ),
    ]
