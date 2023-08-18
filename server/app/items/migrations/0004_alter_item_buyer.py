# Generated by Django 4.2.3 on 2023-08-17 09:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("items", "0003_alter_item_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="item",
            name="buyer",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="buy_item",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
