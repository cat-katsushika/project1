# Generated by Django 4.2.3 on 2023-08-19 01:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("items", "0004_alter_item_buyer"),
    ]

    operations = [
        migrations.RenameField(
            model_name="image",
            old_name="photo",
            new_name="photo_url",
        ),
        migrations.AddField(
            model_name="image",
            name="order",
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="item",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
