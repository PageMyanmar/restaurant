# Generated by Django 5.1.1 on 2025-01-13 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0004_remove_productmodel_quantity_productmodel_stock"),
    ]

    operations = [
        migrations.AddField(
            model_name="cartmodel",
            name="takeaway",
            field=models.BooleanField(default=False),
        ),
    ]
