# Generated by Django 4.1.6 on 2023-03-11 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0014_alter_product_specifications"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="specifications",
            field=models.JSONField(),
        ),
    ]
